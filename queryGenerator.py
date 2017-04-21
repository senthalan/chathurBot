from configReader import read_config

table_name = read_config("tableName")
equality_map = {"greater": ">=", "less": "<=", "equal": "="}
entity_map = {"number": "memory", "amount_of_money": "price", "model": "model", "company": "company", "onlineStore": "onlineStore"}


def generate_query(response):
    query_template = u"SELECT DISTINCT {function}({column_name}) FROM {table_name} {where_expression} {order_expression}"
    entities_list = {}
    intent = ''
    select = ''
    equality = ''
    max_min = ''
    order_part = ''

    # reading the response
    for key in response:
        if key == 'intent':
            intent = ((response[key])[0])['value']
            print "intent : " + intent
        else:
            entities = (response[key])
            values = []
            for entity in entities:
                values.append(entity['value'])
            entities_list[key] = values

    # spilt the intent and divide into cases
    intent_split = intent.split('_')

    # case columnName_equality
    if len(intent_split) == 2:
        select = intent_split[0]
        equality = intent_split[1]
    elif len(intent_split) == 3:
        # case Max/Min_columnName_equality
        if (intent_split[0] == "Max") or (intent_split[0] == "Min"):
            max_min = intent_split[0]
            select = intent_split[1]
            equality = intent_split[2]
        # case Model_max_price
        else:
            select = intent_split[0]
            order = intent_split[1]
            order_by = intent_split[2]
            order_part = build_order_template(order, order_by)

    # joining the queries
    where_part = build_where_template(entities_list, equality)
    select = select.lower()

    final_query = query_template.format(function=max_min, column_name=select, table_name=table_name,
                                        where_expression=where_part, order_expression=order_part)
    return final_query


def build_where_template(entities_list, equality):
    where_template = u"{entity_key} {equality} {entity_value}"
    where_between_template = u"{entity_key} BETWEEN {entity_value_one} AND {entity_value_two}"
    where_list = []
    keys = entities_list.keys()
    for key in keys:
        entity_value = entities_list.pop(key, None)
        if (key == "number") or (key == "amount_of_money"):
            if equality != "between":
                where_query = where_template.format(entity_key=entity_map[key], equality=equality_map[equality],
                                                    entity_value=str(entity_value[0]))
                where_list.append(where_query)
            else:
                where_query = where_between_template.format(entity_key=entity_map[key],
                                                            entity_value_one=str(entity_value[0]),
                                                            entity_value_two=str(entity_value[1]))
                where_list.append(where_query)
        else:
            where_query = where_template.format(entity_key=key, equality=equality_map["equal"],
                                                entity_value="\"" + entity_value[0] + "\"")
            where_list.append(where_query)
    final_where = ""
    for i in range(0, len(where_list)):
        if (i == 0):
            final_where += "WHERE "
        final_where += where_list[i] + " "
        if i != len(where_list) - 1:
            final_where += "AND "
    return final_where


def build_order_template(order, order_by):
    order_template = u"ORDER BY {order_by} {order} LIMIT 1"
    if order.lower() == "max":
        order = "DES"
    elif order.lower() == "min":
        order = "ASC"
    order_part = order_template.format(order_by=order_by, order=order)
    return order_part

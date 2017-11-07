from configReader import read_config

table_name = read_config("tableName")


def generate_query(intent, entities_list, extremum, comparator, order_by, order, limit):
    query_template = u"SELECT DISTINCT {function}({column_name}) FROM {table_name} {where_expression} {order_expression}"

    select = intent.lower()

    # joining the queries
    where_part = build_where_template(entities_list, comparator)

    order_part = build_order_template(order, order_by)

    final_query = query_template.format(function=extremum, column_name=select, table_name=table_name,
                                        where_expression=where_part, order_expression=order_part)
    return final_query


def build_where_template(entities_list, comparator):
    where_template = u"{entity_key} {equality} {entity_value}"
    where_between_template = u"{entity_key} BETWEEN {entity_value_one} AND {entity_value_two}"
    where_list = []
    keys = entities_list.keys()
    for key in keys:
        entity_value = entities_list.pop(key, None)
        if (key == "price") or (key == "memory"):
            if comparator != "between":
                where_query = where_template.format(entity_key=key, equality=comparator,
                                                    entity_value=str(entity_value[0]))
                where_list.append(where_query)
            else:
                where_query = where_between_template.format(entity_key=key,
                                                            entity_value_one=str(entity_value[0]),
                                                            entity_value_two=str(entity_value[1]))
                where_list.append(where_query)
        else:
            temp = entity_value[0].split()
            value = '%'
            for val in temp:
                value = value + val + '%'
            where_query = where_template.format(entity_key=key, equality='like',
                                                entity_value="\"" + value + "\"")
            where_list.append(where_query)
    final_where = ""
    for i in range(0, len(where_list)):
        if i == 0:
            final_where += "WHERE "
        final_where += where_list[i] + " "
        if i != len(where_list) - 1:
            final_where += "AND "
    return final_where


def build_order_template(order, order_by):
    order_template = u"ORDER BY {order_by} {order}  LIMIT 1"
    order_part = ''
    if order_by != '':
        order_part = order_template.format(order_by=order_by, order=order)
    return order_part

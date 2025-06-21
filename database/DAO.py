from database.DB_connect import DBConnect
from model.arco import Arco
from model.orders import Order
from model.store import Store


class DAO():
    def getAllOrders(store_id):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from orders o
                    where o.store_id = %s"""

        cursor.execute(query,(store_id,))


        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from stores s"""

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    def getAllArchi(store_id,k):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select o1.order_id as id1, o2.order_id as id2, count(o3.quantity+o4.quantity) as peso
                    from orders o1 , orders o2 , order_items o3,  order_items o4
                    where o1.store_id = %s
                    and o1.store_id = o2.store_id
                    and o1.order_id = o3.order_id
                    and o2.order_id = o4.order_id
                    and o1.order_date > o2.order_date
                    and DATEDIFF(o1.order_date, o2.order_date)< %s
                    group by id1 , id2"""

        cursor.execute(query, (store_id,k,))

        for row in cursor:
            results.append(Arco(**row))

        cursor.close()
        conn.close()
        return results

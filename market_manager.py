import sqlite3
from random import randint

from database_manager import query_item, update_item
from . import database_manager
# 连接到SQLite数据库
# 数据库文件是market.db
conn = sqlite3.connect('market.db')
cursor = conn.cursor()

# 创建一个表格用于存储销售信息，包括卖家ID
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    seller_id TEXT NOT NULL,
    item TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    exchange_item TEXT NOT NULL,
    exchange_quantity INTEGER NOT NULL
)
''')

# 提交事务
conn.commit()

def sell(seller_id, item, quantity, exchange_item, exchange_quantity):
    """卖家使用此函数来发布销售信息"""
    seller_id = str(seller_id)  # 确保ID是字符串
    # 生成一个随机ID
    sale_id = randint(1000, 9999)
    # 将销售信息插入到数据库
    cursor.execute('''
    INSERT INTO sales (id, seller_id, item, quantity, exchange_item, exchange_quantity)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (sale_id, seller_id, item, quantity, exchange_item, exchange_quantity))
    conn.commit()
    return sale_id

def buy(buyer_id, sale_id):
    """买家使用此函数来执行购买"""
    buyer_id = str(buyer_id)  # 确保ID是字符串
    # 从数据库中获取销售信息
    cursor.execute('SELECT * FROM sales WHERE id=?', (sale_id,))
    sale = cursor.fetchone()
    if sale:
        seller_id, item, quantity, exchange_item, exchange_quantity = sale[1], sale[2], sale[3], sale[4], sale[5]
        # 检查买家和卖家是否有足够物品
        if query_item(buyer_id, exchange_item) >= exchange_quantity and query_item(seller_id, item) >= quantity:
            # 更新买家和卖家的物品数量
            update_item(buyer_id, exchange_item, -exchange_quantity)
            update_item(seller_id, item, -quantity)
            update_item(buyer_id, item, quantity)
            update_item(seller_id, exchange_item, exchange_quantity)
            # 确认交易后，移除该销售信息
            cursor.execute('DELETE FROM sales WHERE id=?', (sale_id,))
            conn.commit()
            print(f"交易成功，ID为{sale_id}的销售信息已被移除。")
        else:
            print("交易失败，买家或卖家物品数量不足。")
    else:
        print("交易失败，未找到该ID的销售信息。")

# 示例使用
# 卖家发布销售信息
seller_id = 'seller123'  # 假设的卖家ID
sale_id = sell(seller_id, '苹果', 10, '香蕉', 5)
print(f"销售信息已发布，ID为: {sale_id}")

# 买家执行购买
buyer_id = 'buyer456'  # 假设的买家ID
buy(buyer_id, sale_id)

# 关闭数据库连接
conn.close()

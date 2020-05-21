from models.database import Database as db_conn

class Category(db_conn):
    def __init__(self, data=None):
        if data is not None:
                self.category_name=data[0]
    
    def create_category(self):
        query="INSERT INTO category (category_name) VALUES (?)"
        values=(self.category_name,)

        result=self.saving_or_editing(query,values)

    def view_all_category(self):
        query="SELECT * FROM category"
        result=self.fetch_all_rows(query)
        
        return result

    def view_single_category(self,id):
        query="select * from category where id = ?"
        values=(id,)
        result=self.fetch_single_row(query,values)
        return result
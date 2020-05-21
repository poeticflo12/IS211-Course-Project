from models.database import Database as db_conn

class Post(db_conn):
    def __init__(self, data=None):
        if data is not None:
            self.author=data[0]
            self.title=data[1]
            self.content=data[2]
            self.publish_date=data[3]
            self.permalink=data[4]
            self.isPublish=data[5]
            self.category_id=data[6]
    
    def create_post(self):
        query="INSERT INTO post (author,title,content,publish_date,permalink,isPublished,category_id) values (?,?,?,?,?,?,?)"
        values=(self.author,self.title,self.content,self.publish_date,self.permalink,self.isPublish,self.category_id)
        result=self.saving_or_editing(query,values)
        return result
    
    def view_all_post(self):
        query="""SELECT p.title, p.content, p.publish_date, p.permalink, u.username, c.category_name,c.id FROM post p 
        inner join category c on c.id=p.category_id 
        inner join user u on u.id = p.author
        WHERE isPublished=1 ORDER BY publish_date DESC"""
        result=self.fetch_all_rows(query)
        return result
    
    def view_by_author(self,id):
        query="SELECT * FROM post where author=(?)"
        values=(id,)
        result=self.fetch_all_rows_by_id(query,values)
        return result
    
    def view_single_post(self,permalink):
        query="SELECT *,j.category_name FROM post inner join category j on post.category_id = j.id WHERE author=(?)"
        values=(permalink,)
        result=self.fetch_single_row(query,values)
        return result
    
    def update_post(self, value, user_id):
        query="UPDATE post SET title=?, content=?, category_id=? where author=?"
        title=value[0]
        content=value[1]
        category_id=value[2]
        values=(title,content,category_id,user_id)
        result=self.saving_or_editing(query,values)
        return result
    
    def unpublish(self, post_id):
        query="UPDATE post SET isPublished=0 where id= ?"
        values=(post_id,)
        print(post_id)
        result=self.saving_or_editing(query,values)
        return result

    def publish(self, post_id):
        query="UPDATE post SET isPublished=1 where id= ?"
        values=(post_id,)
        print(post_id)
        result=self.saving_or_editing(query,values)
        return result
    
    def delete_post(self, id):
        query="DELETE from post where id = ?"
        values=(id,)
        result=self.delete_row(query,values)
        return result
    
    def view_by_permalink(self,permalink):
        query="""SELECT p.title, p.content, p.publish_date, p.permalink, u.username, c.category_name,c.id FROM post p 
        inner join category c on c.id=p.category_id 
        inner join user u on u.id = p.author
        WHERE p.permalink= ?"""
        values=(permalink,)
        result=self.fetch_single_row(query,values)
        return result
    
    def view_by_category(self, category):
        query="""SELECT p.title, p.content, p.publish_date, p.permalink, u.username, c.category_name,c.id FROM post p 
        inner join category c on c.id=p.category_id 
        inner join user u on u.id = p.author
        WHERE p.category_id= ?"""
        values=(category,)
        result=self.fetch_all_rows_by_id(query,values)
        return result
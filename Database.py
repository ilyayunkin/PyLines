import sqlite3


class Database:
    def __init__(self):
        self.max_scores = 3
        self.hscores_table_name = 'hscores'
        self.db = sqlite3.connect("highscores.db")
        self.cursor = self.db.cursor()
        self.create_table()
        self.get_scores_count()
        self.get_minimal_score()

    def create_table(self):
        try:
            self.get_scores()
        except sqlite3.OperationalError:
            q = "CREATE TABLE " + self.hscores_table_name + ' (name TEXT, scores INTEGER);'
            print(q)
            self.cursor.execute(q)

    def get_scores(self):
        q = "SELECT * FROM " + self.hscores_table_name + ' ORDER BY scores DESC;'
        print(q)
        self.cursor.execute(q)
        scores_list = self.cursor.fetchall()
        print(scores_list)
        return scores_list

    def score_is_high(self, scores_list, coins):
        save_score = True
        if scores_list.__len__() >= self.max_scores:
            minimal = self.get_minimal_score()
            if minimal >= coins:
                save_score = False

        return save_score

    def save_score(self, name, coins):
        print("name =" + name)
        q = "INSERT INTO " + self.hscores_table_name + " (name, scores) " + \
            "VALUES ('" + name + "', '" + str(coins) + "');"
        print(q)
        self.cursor.execute(q)
        self.db.commit()

    def get_minimal_score(self):
        q = 'SELECT min(scores) FROM ' + self.hscores_table_name;
        print(q)
        self.cursor.execute(q)
        minimal = int(self.cursor.fetchone()[0])
        print('minimal_score = ' + str(minimal))
        return minimal

    def get_scores_count(self):
        q = 'SELECT count(*) FROM ' + self.hscores_table_name;
        print(q)
        self.cursor.execute(q)
        count = int(self.cursor.fetchone()[0])
        print('scores count = ' + str(count))
        return count

    def delete_extra_scores(self):
        while self.get_scores_count() > self.max_scores:
            self.delete_scores_less_than(self.get_minimal_score())

    def delete_scores_less_than(self, minimal):
        q = "DELETE FROM " + self.hscores_table_name + \
            " WHERE scores <= " + str(minimal)
        print(q)
        self.cursor.execute(q)
        self.db.commit()

    def get_max_scores(self):
        return self.max_scores

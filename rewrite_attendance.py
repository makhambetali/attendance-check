import sqlite3

def rewrite_attendance():
    conn = sqlite3.connect('attendance1.db')
    cur = conn.cursor()
    cur.execute('UPDATE students SET attended = 0')
    conn.commit()
    conn.close()
    print('Attendance reset done.')

if __name__ == '__main__':
    rewrite_attendance()

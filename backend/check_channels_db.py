import sqlite3

conn = sqlite3.connect('config/channels.db')
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(saved_channels)')
columns = cursor.fetchall()
print('Estrutura da tabela saved_channels:')
for col in columns:
    print(f'{col[1]} ({col[2]})')

print('\nConteúdo da tabela saved_channels:')
cursor.execute('SELECT * FROM saved_channels')
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
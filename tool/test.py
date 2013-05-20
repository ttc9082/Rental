from rentaldb import *

# x=SQL_init()

# x.create_user_table()
# x.create_room_table()

# x.drop_tables()

# user_data=[ "zz", "zzpassword", "zz@zz.com", "1234", 1]
# user1= User()
# user1.insert(user_data)
# print user1.uid

# room_data=[1, "new apartment in brooklyn", "1 bathroom, 1 bedroom", "brooklyn", "900", "bucket", 0]
# rm1  = Room()
# rm1.insert(room_data)
# print rm1.rid

p=User.validate_passwd("zz")

print type(p)
from rentaldb import *

# SETUP.drop_tables()

# SETUP.create_user_table()
# SETUP.create_room_table()

# user_data=[ "zz", "zzpassword", None, "1234", 1]
# User.insert(user_data)

# room_data=[1, "new apartment in brooklyn", "1 bathroom, 1 bedroom", "brooklyn", "900", "bucket", 0]
# Room.insert(room_data)

# p=User.validate_passwd("zz")
u=User.find_by_id(1)
print u[1]
# rs= Room.show_all()
# print len(rs)
# myroom = Room.show_my_rooms(1)
# print myroom

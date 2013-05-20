from rentaldb import *


# SETUP.drop_tables()

SETUP.create_user_table()
SETUP.create_room_table()

# user_data=[ "zz", "foobar", None, "1234", 1]
# User.insert(user_data)

# room_data=[1, "new apartment in brooklyn", "1 bathroom, 1 bedroom", "brooklyn", "900", "bucket", 0]
# Room.insert(room_data)

# ps=User.validate_passwd("zz")
# my="z"
# for p in ps:
#     if my==p[0]:
#         id = p[1]
# print id

# u=User.find_by_id(1)
# rs= Room.show_all()
# print len(rs)
# print rs
# myroom = Room.show_my_rooms(1)
# print myroom
# bname = Room.find_by_id(13)
# print bname
# print bname[6]

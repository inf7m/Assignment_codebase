from Logs_Ops_class import *

log_ops_instace = Logs_Ops_class(log_directory="/logs")

# Un-comment to test
# log_ops_instace.query1(from_datetime="2020-02-01",to_datetime="2020-02-20",user="user1",granularity="1day")

# log_ops_instace.query2(from_datetime="2020-02-01", to_datetime="2020-02-20", user="user1", app="app2",
#                        granularity="30min")

log_ops_instace.query3(from_datetime="2020-02-01", to_datetime="2020-02-20", user="user1", granularity="1day",
                       group_by="app")

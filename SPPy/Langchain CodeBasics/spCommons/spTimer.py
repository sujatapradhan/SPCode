import datetime
import pytz
class spTimer:
    def ShowTime(func): 
        def wrapper_function(*args, **kwargs): #to help variable parameter passing
            import time
            start = time.time()
            func(*args,  **kwargs) 
            end = time.time()
            print("The time of execution of ",func.__name__," is :",(end-start) * 10**3, "ms")
        return wrapper_function 
    def spISOToUTC(iso_datetime_str):
        import datetime
        # create or pass iso string
        # iso_datetime_str = "2024-04-30T12:00:00"  # Example datetime in ISO format
        # Convert ISO-formatted string to datetime object
        # from datetime import datetime
        import pytz
        # Example ISO-formatted datetime string
        # Convert ISO-formatted string to datetime object
        datetime_obj = datetime.datetime.fromisoformat(iso_datetime_str)
        # Make the datetime object timezone-aware (assuming it's in UTC)
        utc_aware_datetime = datetime_obj.replace(tzinfo=pytz.UTC)
        return utc_aware_datetime
    def spNaiveToUTC(naive_datetime, timezone):
        import datetime
        import pytz
        # Create/pass a naive datetime object
        #naive_datetime = datetime.datetime(2024, 4, 30, 12, 0, 0)  # Example datetime (year, month, day, hour, minute, second)
        # Choose the desired time zone
        desired_timezone = pytz.timezone(timezone) # 'Your/Desired/Timezone')  # Replace 'Your/Desired/Timezone' with the appropriate time zone string
        # Convert the naive datetime to an offset-aware datetime
        offset_aware_datetime = desired_timezone.localize(naive_datetime)
        return offset_aware_datetime   
    


def directShowTime(func): 
    def wrapper_function(*args, **kwargs):  #to help variable parameter passing
      import time
      start = time.time()
      func(*args,  **kwargs) 
      end = time.time()
      print("The time of execution of ",func.__name__," is :",(end-start) * 10**3, "ms")
    return wrapper_function 
  
  
@spTimer.ShowTime
def say_hello(): 
    print("Hello Geeks!") 
  
def say_bye(): 
    print("Bye Geeks!") 
say_bye = spTimer.ShowTime(say_bye)
 
if __name__ == "__main__":
    print("Directly called")
    say_hello() 
    say_bye() 
else:
    pass



print(str(spTimer.spISOToUTC("2003-03-30T12:33:33")))
print(str(spTimer.spNaiveToUTC(datetime.datetime(2003, 3, 30, 3, 33, 33) ,"utc")))
#2024-04-30T00:00datetime.datetime(2024, 4, 30, 12, 0, 0))))  # Example datetime (year, month, day, hour, minute, second)
    
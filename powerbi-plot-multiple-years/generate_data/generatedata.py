from calendar import month
import datetime
from datetime import timedelta
from fileinput import filename
import random
import os.path
import os

def generate_date(start_date:datetime.datetime, days:int):
    print("Generating time series data")
    filename="sales.csv"
    if (os.path.exists(filename)):
        print(f"Deleted file {filename}")
        os.remove(filename)
    
    target_date=start_date + timedelta(days=days)
    current_date=start_date
    day_index=0
    max_percentage_daily_rise=1
    base_sales=current_date.year*10

    f=open(file=filename,mode="a")
    f.write("date,sales\n")
    while (current_date < target_date):
        #base_sales=current_date.year*10
        datestr=current_date.strftime("%Y-%m-%d")
        #new_sales=random.randint(base_sales,base_sales+3)
        percentage_daily_with_noise=  -max_percentage_daily_rise + random.random() *2* max_percentage_daily_rise

        new_sales=base_sales + base_sales* percentage_daily_with_noise/100.0 
        base_sales=new_sales
        line=f"{datestr},{new_sales}\n"
        print(line)
        current_date=current_date+timedelta(days=1)
        day_index+=1
        f.write(line)
    f.close()

if __name__ == "__main__":
    start_date=datetime.datetime(2012, 5, 17)
    num_months=30
    generate_date(start_date=start_date, days=num_months*30)


import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def tura(day, month, service, work_from, ora_start, ora_sfarsit):
    
    if work_from == "WFH":
        location = "HOME"
    else:
        location = "OFFICE"
    
    
    tura = {
        "summary": f"{work_from} Helpdesk",
        "location": location,
        "description": location,
        "colorId": 3,
        "start": {
            "dateTime": f"2025-{month}-{day}T{ora_start}:00+02:00",
            "timeZone": "Europe/Bucharest"
        },
        "end": {
            "dateTime": f"2025-{month}-{day}T{ora_sfarsit}:00+02:00",
            "timeZone": "Europe/Bucharest"
        },
    }
    IDfile = open("CalendarID.txt")
    event = service.events().insert(calendarId=IDfile.read(), body=tura).execute()
    event = service.events().insert(calendarId="primary", body=tura).execute()
    print(f"eveniment creat {event.get('htmlLink')}")
    print(location, day)
    return 0
    


def main():
    creds = None
    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file(
              "credentials.json", SCOPES
          )
          creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
          token.write(creds.to_json())
          
    try:
        service = build("calendar", "v3", credentials=creds)
        
        now = dt.datetime.now().isoformat() + "Z"
        zi = f"0{3}"
        variable = f"2025-02-{zi}T09:00:00+02:00"
        

        event = {
            "summary": "test",
            "location": "",
            "description": "teest",
            "colorId": 3,
            "start": {
                "dateTime": variable,
                "timeZone": "Europe/Bucharest"
            },
            "end": {
                "dateTime": "2025-02-03T17:00:00+02:00",
                "timeZone": "Europe/Bucharest"
            },
        }

        shifts_input = open("shifts.txt","r")
        shifts = []
        #THIS || NEXT
        
        v = str(dt.date.today()).split("-")
        #print(v)
        current_month = v[1]
        which_month = shifts_input.readline()
        if which_month == "THIS\n":
            x = dt.datetime(2025,int(current_month)+1,1)
            print(x)
            print(x-dt.timedelta(days=1))
            next_month = str(x-dt.timedelta(days=1)).split()
            next_month = next_month[0].split("-")
            print(next_month)
            last_day_of_current_month = next_month[2]
            #print(last_day_of_current_month)
        elif which_month == "NEXT\n":
            x = str(dt.datetime(2025,int(current_month)+1,1))
            v = x.split("-")
            current_month = v[1]
            x = dt.datetime(2025,int(current_month)+1,1)
            print(x)
            print(x-dt.timedelta(days=1))
            next_month = str(x-dt.timedelta(days=1)).split()
            next_month = next_month[0].split("-")
            print(next_month)
            last_day_of_current_month = next_month[2]
            print(last_day_of_current_month)
            
        

        for shift in shifts_input:
            shifts.append(shift.split())
        print(shifts)
        
        day = 1
                
        
        
        #event = service.events().insert(calendarId="primary", body=event).execute()
        #print(f"eveniment creat {event.get('htmlLink')}")
        
    except HttpError as error:
        print("AN ERROR HAS OCCURRED", error)
    
    
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print(calendar_list_entry['summary'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    
    for shift in shifts:
        if shift[0] != 'l' and shift[0] != 'L':
            if shift[1] == '0':
                work_from = "WFH"
            elif shift[1] == '1':
                work_from = "WFO"
            if shift[0] == '1':
                ora_start = "05:30"
                ora_sfarsit = "14:30"
            elif shift[0] == '2':
                ora_start = "14:00"
                ora_sfarsit = "23:00"
            elif shift[0] == '3':
                ora_start = "09:00"
                ora_sfarsit = "18:00"
            tura(day, current_month, service, work_from, ora_start, ora_sfarsit)
        day += 1
        
    



    '''
        elif shift[0] == 2:
            if shift[1] == 0:
                tura2wfh(day,current_month, service)
            else:
                tura2wfo(day,current_month, service)
        elif shift[0] == 3:
            if shift[1] == 0:
                tura3wfh(day,current_month, service)
            else:
                tura3wfo(day,current_month, service)
    '''
        
        
if __name__ == "__main__":
    main()
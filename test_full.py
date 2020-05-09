import airport_weather
import time

def test_csv_lookup():
    airport_ids = [
        "01KY",
        "01LA",
        "01LL",
        "01LS",
        "01MA",
        "01MD",
        "something",
        "01ME",
        "that",
        "01MI",
        "01MN",
        "01MO",
        "doesn't",
        "make",
        "sense",
        "01MT",
        "01NC"
    ]
    
    valid_airports = 12
    count = 0
    for id in airport_ids:
        a = airport_weather.Airport(id)
        if (a.name != None):
            count += 1
    
    assert count == valid_airports

def test_get_conditions():
    airport_ids = [
        "01KY",
        "01LA",
        "01LL",
        "01LS",
        "01MA",
        "01MD",
        "something",
        "01ME",
        "that",
        "01MI",
        "01MN",
        "01MO",
        "doesn't",
        "make",
        "sense",
        "01MT",
        "01NC"
    ]

    valid_airports = 12
    count = 0
    for airport_id in airport_ids:
        a = airport_weather.Airport(airport_id)
        c = a.get_current_conditions()
        print(c)
        if (c["valid"]):
            count += 1
        time.sleep(0.5)

    assert count == valid_airports

if __name__ == "__main__":
    test_get_conditions()
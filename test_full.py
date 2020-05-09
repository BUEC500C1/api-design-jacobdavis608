import airport_weather

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
        "01NC",
        "01NE"
    ]
    
    valid_airports = 13
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
        "01NC",
        "01NE"
    ]

    valid_airports = 13
    count = 0
    for id in airport_ids:
        a = airport_weather.Airport(id)
        c = a.get_current_conditions()
        if (len(c.keys()) > 1): #valid data
            count += 1

    assert count == valid_airports


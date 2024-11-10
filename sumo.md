```mermaid
classDiagram
    class Scrape {
        - String url
        - Int max_page
        + load_page(url: String)
        + scrape()
        + measure_time()
    }

    class DataSample {
        + get_data()
    }

    class DataHome {
        + String category
        + String name
        + String address
        + String near_station
        + Int age_and_floors
    }

    class DataRoom {
        + Int floor 
        + Int price_and_price_administration
        + Int price_deposit_and_gratuity
        + String madori_and_menseki
        + String url
    }

    Scrape --> DataSample : 
    DataSample <|-- DataHome : 
    DataSample <|-- DataRoom : 
```


from bs4 import BeautifulSoup
from building import Building
from room import Room

class Parser:
    def parse_page(self, soup: BeautifulSoup):
        """1ページ分のデータをパース"""
        buildings = soup.find_all(class_='cassetteitem')
        return [room for building in buildings for room in self.parse_building_with_rooms(building)]

    def parse_building_with_rooms(self, building) -> list:
        """建物データと部屋データをまとめてパース"""
        # 建物データの作成
        building_data = self.parse_building(building)
        # 部屋データの作成
        rooms = building.find(class_='cassetteitem_other')
        return self.parse_rooms(rooms, building_data)

    def parse_building(self, building) -> Building:
        """建物データをパース"""
        name = building.find(class_='cassetteitem_content-title').text
        address = building.find(class_='cassetteitem_detail-col1').text

        # 最寄り駅の情報を取得
        stations = [
            station.text
            for station in building.find(class_='cassetteitem_detail-col2').find_all(class_='cassetteitem_detail-text')
        ]

        # 築年数と階数
        details = building.find(class_='cassetteitem_detail-col3').find_all('div')
        age, floors = (details[0].text, details[1].text) if len(details) >= 2 else ("", "")

        return Building(name=name, address=address, stations=stations, age=age, floors=floors)

    def parse_rooms(self, rooms, building: Building) -> list:
        """部屋データをパース"""
        return [
            self.parse_room(room, building)
            for room in rooms.find_all(class_='js-cassette_link')
        ]

    def parse_room(self, room, building: Building) -> Room:
        """1部屋分のデータをパース"""
        tds = room.find_all('td')

        floor = tds[2].text.strip()
        rent = tds[3].find(class_='cassetteitem_other-emphasis ui-text--bold').text
        management_fee = tds[3].find(class_='cassetteitem_price cassetteitem_price--administration').text
        deposit = tds[4].find(class_='cassetteitem_price cassetteitem_price--deposit').text
        gratuity = tds[4].find(class_='cassetteitem_price cassetteitem_price--gratuity').text
        layout = tds[5].find(class_='cassetteitem_madori').text
        size = tds[5].find(class_='cassetteitem_menseki').text
        url = tds[8].find(class_='js-cassette_link_href cassetteitem_other-linktext').get('href')

        return Room(
            building=building,
            floor=floor,
            rent=rent,
            management_fee=management_fee,
            deposit=deposit,
            gratuity=gratuity,
            layout=layout,
            size=size,
            url=url
        )
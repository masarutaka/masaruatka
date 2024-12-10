from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List
from model.Building import Building
from model.Room import Room

class Parser:
    def parse_page(self, soup: BeautifulSoup) -> List[Room]:
        """1ページ分のデータをパース"""
        buildings: List[Tag] = soup.find_all(class_='cassetteitem')
        return [room for building in buildings for room in self.parse_building_with_rooms(building)]

    def parse_building_with_rooms(self, building: Tag) -> List[Room]:
        """建物データと部屋データをまとめてパース"""
        # 建物データの作成
        building_data: Building = self.parse_building(building)
        # 部屋データの作成
        rooms: Tag = building.find(class_='cassetteitem_other')
        return self.parse_rooms(rooms, building_data)

    def parse_building(self, building: Tag) -> Building:
        """建物データをパース"""
        # 建物名の取得
        name: str = building.find(class_='cassetteitem_content-title').text.strip()

        # 住所の取得
        address: str = building.find(class_='cassetteitem_detail-col1').text.strip()

        # 最寄り駅の情報を取得
        stations: List[str] = [
            station.text.strip()
            for station in building.find(class_='cassetteitem_detail-col2').find_all(class_='cassetteitem_detail-text')
        ]

        # 築年数と階数
        details: List[Tag] = building.find(class_='cassetteitem_detail-col3').find_all('div')
        age: str = details[0].text.strip() if len(details) > 0 else ""
        floors: str = details[1].text.strip() if len(details) > 1 else ""

        return Building(name=name, address=address, stations=stations, age=age, floors=floors)

    def parse_rooms(self, rooms: Tag, building: Building) -> List[Room]:
        """部屋データをパース"""
        return [
            self.parse_room(room, building)
            for room in rooms.find_all(class_='js-cassette_link')
        ]

    def parse_room(self, room: Tag, building: Building) -> Room:
        """1部屋分のデータをパース"""
        # テーブルデータの取得
        tds: List[Tag] = room.find_all('td')

        # 各データの抽出
        floor: str = tds[2].text.strip()
        rent: str = tds[3].find(class_='cassetteitem_other-emphasis ui-text--bold').text.strip()
        management_fee: str = tds[3].find(class_='cassetteitem_price cassetteitem_price--administration').text.strip()
        deposit: str = tds[4].find(class_='cassetteitem_price cassetteitem_price--deposit').text.strip()
        gratuity: str = tds[4].find(class_='cassetteitem_price cassetteitem_price--gratuity').text.strip()
        layout: str = tds[5].find(class_='cassetteitem_madori').text.strip()
        size: str = tds[5].find(class_='cassetteitem_menseki').text.strip()
        url: str = tds[8].find(class_='js-cassette_link_href cassetteitem_other-linktext').get('href')

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
from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List
from model.Building import Building
from model.Room import Room

class Parser:
    def parse_page(self, soup: BeautifulSoup) -> List[Room]:
        """
        HTMLページ全体から部屋データを抽出する関数。
        - 各建物を取得して、部屋ごとのデータをまとめる。
        """
        # ページ内のすべての建物データを取得
        building_tags: List[Tag] = soup.find_all(class_='cassetteitem')

        # 各建物データを処理して、部屋リストを取得
        all_rooms: List[Room] = []
        for building_tag in building_tags:
            building_rooms = self.parse_building_with_rooms(building_tag)
            all_rooms.extend(building_rooms)
        return all_rooms

    def parse_building_with_rooms(self, building_tag: Tag) -> List[Room]:
        """
        1つの建物から、その建物の部屋リストを取得する関数。
        """
        # 建物データの取得
        building_data: Building = self.parse_building(building_tag)

        # 部屋データの取得
        rooms_section: Tag = building_tag.find(class_='cassetteitem_other')
        room_list: List[Room] = self.parse_rooms(rooms_section, building_data)
        return room_list

    def parse_building(self, building_tag: Tag) -> Building:
        """
        1つの建物情報（名前、住所、最寄り駅など）を取得してBuildingオブジェクトを作成する関数。
        """
        # 建物名の取得
        name: str = building_tag.find(class_='cassetteitem_content-title').text.strip()

        # 住所の取得
        address: str = building_tag.find(class_='cassetteitem_detail-col1').text.strip()

        # 最寄り駅の情報を取得
        stations: List[str] = [
            station.text.strip()
            for station in building_tag.find(class_='cassetteitem_detail-col2').find_all(class_='cassetteitem_detail-text')
        ]

        # 築年数と階数を取得
        details: List[Tag] = building_tag.find(class_='cassetteitem_detail-col3').find_all('div')
        age: str = details[0].text.strip() if len(details) > 0 else ""
        floors: str = details[1].text.strip() if len(details) > 1 else ""

        # Buildingデータを作成して返す
        return Building(name=name, address=address, stations=stations, age=age, floors=floors)

    def parse_rooms(self, rooms_section: Tag, building: Building) -> List[Room]:
        """
        部屋データのセクションから、各部屋をRoomオブジェクトとしてリストで取得する関数。
        """
        # 部屋データのリストを作成
        room_list: List[Room] = []
        room_tags = rooms_section.find_all(class_='js-cassette_link')
        for room_tag in room_tags:
            room_data = self.parse_room(room_tag, building)
            room_list.append(room_data)
        return room_list

    def parse_room(self, room_tag: Tag, building: Building) -> Room:
        """
        1つの部屋のデータをRoomオブジェクトとして取得する関数。
        """
        # 部屋データの各値を取得
        tds: List[Tag] = room_tag.find_all('td')

        floor: str = tds[2].text.strip()
        rent: str = tds[3].find(class_='cassetteitem_other-emphasis ui-text--bold').text.strip()
        management_fee: str = tds[3].find(class_='cassetteitem_price cassetteitem_price--administration').text.strip()
        deposit: str = tds[4].find(class_='cassetteitem_price cassetteitem_price--deposit').text.strip()
        gratuity: str = tds[4].find(class_='cassetteitem_price cassetteitem_price--gratuity').text.strip()
        layout: str = tds[5].find(class_='cassetteitem_madori').text.strip()
        size: str = tds[5].find(class_='cassetteitem_menseki').text.strip()
        url: str = tds[8].find(class_='js-cassette_link_href cassetteitem_other-linktext').get('href')

        # Roomデータを作成して返す
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

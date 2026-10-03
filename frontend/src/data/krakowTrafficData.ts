export interface TrafficPoint {
  id: string
  name: string
  district: string
  lat: number
  lng: number
  description: string
  congestionBase: number // 0-100%
  cameraUrl?: string
}

export interface TrafficStreet {
  id: string
  name: string
  district: 'Centrum' | 'Północ' | 'Południe' | 'Nowa Huta' | 'Zachód'
  coordinates: [number, number][]
  morningPeak: number // 07:00 - 09:30 (% zakorkowania)
  afternoonPeak: number // 15:30 - 18:30 (% zakorkowania)
  offPeak: number // godziny pozaszczytowe (% zakorkowania)
  lengthKm: number
  speedLimit: number
}

// Kompletna siatka głównych arterii całego Krakowa
export const krakowStreets: TrafficStreet[] = [
  // ==========================================
  // 1. CENTRUM & I OBWODNICA
  // ==========================================
  {
    id: 'basztowa',
    name: 'ul. Basztowa (I Obwodnica)',
    district: 'Centrum',
    coordinates: [
      [50.0656, 19.9370],
      [50.0650, 19.9410],
      [50.0645, 19.9445],
      [50.0638, 19.9465],
    ],
    morningPeak: 85,
    afternoonPeak: 90,
    offPeak: 30,
    lengthKm: 0.8,
    speedLimit: 50,
  },
  {
    id: 'westerplatte',
    name: 'ul. Westerplatte',
    district: 'Centrum',
    coordinates: [
      [50.0638, 19.9465],
      [50.0610, 19.9445],
      [50.0585, 19.9430],
      [50.0570, 19.9415],
    ],
    morningPeak: 75,
    afternoonPeak: 85,
    offPeak: 25,
    lengthKm: 0.9,
    speedLimit: 50,
  },
  {
    id: 'podwale_dunajewskiego',
    name: 'ul. Dunajewskiego / Podwale',
    district: 'Centrum',
    coordinates: [
      [50.0656, 19.9370],
      [50.0637, 19.9328], // Teatr Bagatela
      [50.0610, 19.9315],
      [50.0580, 19.9330],
      [50.0555, 19.9360],
      [50.0545, 19.9385],
    ],
    morningPeak: 80,
    afternoonPeak: 88,
    offPeak: 35,
    lengthKm: 1.4,
    speedLimit: 50,
  },
  {
    id: 'dietla',
    name: 'ul. Dietla',
    district: 'Centrum',
    coordinates: [
      [50.0545, 19.9385],
      [50.0542, 19.9425],
      [50.0545, 19.9455],
      [50.0555, 19.9500],
      [50.0560, 19.9535],
    ],
    morningPeak: 90,
    afternoonPeak: 95,
    offPeak: 45,
    lengthKm: 1.3,
    speedLimit: 50,
  },
  {
    id: 'karmelicka',
    name: 'ul. Karmelicka',
    district: 'Centrum',
    coordinates: [
      [50.0637, 19.9328],
      [50.0655, 19.9295],
      [50.0675, 19.9260],
    ],
    morningPeak: 80,
    afternoonPeak: 85,
    offPeak: 40,
    lengthKm: 0.7,
    speedLimit: 40,
  },
  {
    id: 'lubicz',
    name: 'ul. Lubicz',
    district: 'Centrum',
    coordinates: [
      [50.0638, 19.9465],
      [50.0645, 19.9500],
      [50.0655, 19.9550],
      [50.0665, 19.9600], // Rondo Mogilskie
    ],
    morningPeak: 92,
    afternoonPeak: 95,
    offPeak: 45,
    lengthKm: 1.1,
    speedLimit: 50,
  },

  // ==========================================
  // 2. ALEJE TRZECH WIESZCZÓW (II Obwodnica)
  // ==========================================
  {
    id: 'aleje_slowackiego',
    name: 'Al. Juliusza Słowackiego',
    district: 'Centrum',
    coordinates: [
      [50.0765, 19.9320], // Nowy Kleparz
      [50.0725, 19.9290],
      [50.0690, 19.9265],
      [50.0665, 19.9245], // Plac Inwalidów
    ],
    morningPeak: 95,
    afternoonPeak: 98,
    offPeak: 55,
    lengthKm: 1.2,
    speedLimit: 50,
  },
  {
    id: 'aleje_mickiewicza',
    name: 'Al. Adama Mickiewicza (AGH / Muzeum)',
    district: 'Centrum',
    coordinates: [
      [50.0665, 19.9245], // Plac Inwalidów
      [50.0620, 19.9230], // AGH
      [50.0585, 19.9235], // Muzeum Narodowe / Kino Kijów
    ],
    morningPeak: 94,
    afternoonPeak: 97,
    offPeak: 50,
    lengthKm: 1.0,
    speedLimit: 50,
  },
  {
    id: 'aleje_krasinskiego',
    name: 'Al. Zygmunta Krasińskiego / Most Dębnicki',
    district: 'Centrum',
    coordinates: [
      [50.0585, 19.9235],
      [50.0535, 19.9260], // Jubilat
      [50.0515, 19.9300], // Most Dębnicki
    ],
    morningPeak: 98,
    afternoonPeak: 99,
    offPeak: 60,
    lengthKm: 0.9,
    speedLimit: 50,
  },

  // ==========================================
  // 3. PÓŁNOC (Opolska / 29 Listopada / Bora-Komorowskiego)
  // ==========================================
  {
    id: 'opolska',
    name: 'ul. Opolska (Trasa Północna)',
    district: 'Północ',
    coordinates: [
      [50.0905, 19.9050], // Węzeł Rondo Ofiar Katynia
      [50.0895, 19.9200],
      [50.0885, 19.9350], // Krowodrza Górka
      [50.0875, 19.9450], // Prądnik Biały
      [50.0855, 19.9650], // Rondo Polsadu
    ],
    morningPeak: 92,
    afternoonPeak: 94,
    offPeak: 40,
    lengthKm: 4.8,
    speedLimit: 70,
  },
  {
    id: 'al_29_listopada',
    name: 'Al. 29 Listopada (Wylot Warszawa)',
    district: 'Północ',
    coordinates: [
      [50.1000, 19.9600], // Granica miasta / Węzeł Północ
      [50.0875, 19.9500], // Skrzyżowanie z Opolską
      [50.0765, 19.9400], // Wiadukt kolejowy
      [50.0700, 19.9440], // Nowy Kleparz / Dworzec
    ],
    morningPeak: 96,
    afternoonPeak: 95,
    offPeak: 45,
    lengthKm: 4.2,
    speedLimit: 60,
  },
  {
    id: 'bora_komorowskiego',
    name: 'Al. Gen. Bora-Komorowskiego',
    district: 'Północ',
    coordinates: [
      [50.0855, 19.9650], // Rondo Polsadu
      [50.0860, 19.9880], // Park Wodny / Serenada
      [50.0840, 20.0050], // Wiadukt Stella-Sawickiego
    ],
    morningPeak: 88,
    afternoonPeak: 90,
    offPeak: 35,
    lengthKm: 3.1,
    speedLimit: 70,
  },

  // ==========================================
  // 4. POŁUDNIE (Konopnickiej / Kamieńskiego / Wielicka / Zakopiańska)
  // ==========================================
  {
    id: 'konopnickiej',
    name: 'ul. Marii Konopnickiej',
    district: 'Południe',
    coordinates: [
      [50.0515, 19.9300], // Most Dębnicki / Rondo Grunwaldzkie
      [50.0450, 19.9340], // Hotel Forum / Wzgórze Lasoty
      [50.0355, 19.9420], // Rondo Matecznego
    ],
    morningPeak: 95,
    afternoonPeak: 97,
    offPeak: 50,
    lengthKm: 2.1,
    speedLimit: 60,
  },
  {
    id: 'kamienskiego',
    name: 'ul. Kamieńskiego',
    district: 'Południe',
    coordinates: [
      [50.0355, 19.9420], // Rondo Matecznego
      [50.0310, 19.9600], // Bonarka City Center
      [50.0240, 19.9750], // Skrzyżowanie z Wielicką / Powstańców Śl.
    ],
    morningPeak: 96,
    afternoonPeak: 95,
    offPeak: 42,
    lengthKm: 3.2,
    speedLimit: 70,
  },
  {
    id: 'zakopianska',
    name: 'ul. Zakopiańska (Wylot na Zakopane)',
    district: 'Południe',
    coordinates: [
      [50.0355, 19.9420], // Rondo Matecznego
      [50.0250, 19.9350], // Łagiewniki / Sanktuarium
      [50.0150, 19.9280], // Borek Fałęcki
      [50.0050, 19.9200], // Węzeł Zakopiański A4
    ],
    morningPeak: 90,
    afternoonPeak: 94,
    offPeak: 40,
    lengthKm: 4.5,
    speedLimit: 60,
  },
  {
    id: 'wielicka',
    name: 'ul. Wielicka (Węzeł Wielicki / A4)',
    district: 'Południe',
    coordinates: [
      [50.0350, 19.9650], // Podgórze / Plac Bohaterów Getta
      [50.0250, 19.9850], // Prokocim Szpital
      [50.0120, 20.0150], // Węzeł Wielicki A4
    ],
    morningPeak: 92,
    afternoonPeak: 93,
    offPeak: 38,
    lengthKm: 5.1,
    speedLimit: 60,
  },
  {
    id: 'trasa_lagiewnicka',
    name: 'Trasa Łagiewnicka / Tischnera',
    district: 'Południe',
    coordinates: [
      [50.0270, 19.9150], // Ruczaj
      [50.0275, 19.9400], // Tunele Łagiewniki
      [50.0280, 19.9650], // Skrzyżowanie z Kamieńskiego
    ],
    morningPeak: 65,
    afternoonPeak: 75,
    offPeak: 20,
    lengthKm: 3.5,
    speedLimit: 70,
  },

  // ==========================================
  // 5. NOWA HUTA & WSCHÓD (Nowohucka / Jana Pawła II / Pokoju)
  // ==========================================
  {
    id: 'nowohucka',
    name: 'ul. Nowohucka / Most Nowohucki',
    district: 'Nowa Huta',
    coordinates: [
      [50.0380, 19.9850], // Skrzyżowanie z Wielicką
      [50.0520, 19.9950], // Most Nowohucki na Wiśle
      [50.0620, 20.0000], // M1 / Al. Pokoju
      [50.0680, 20.0050], // Rondo Czyżyńskie
    ],
    morningPeak: 95,
    afternoonPeak: 96,
    offPeak: 48,
    lengthKm: 4.2,
    speedLimit: 70,
  },
  {
    id: 'mogilska_jana_pawla',
    name: 'ul. Mogilska / Al. Jana Pawła II',
    district: 'Nowa Huta',
    coordinates: [
      [50.0665, 19.9600], // Rondo Mogilskie
      [50.0685, 19.9850], // Tauron Arena Kraków
      [50.0710, 20.0200], // Rondo Czyżyńskie
      [50.0715, 20.0380], // Plac Centralny Nowa Huta
    ],
    morningPeak: 90,
    afternoonPeak: 92,
    offPeak: 38,
    lengthKm: 6.0,
    speedLimit: 60,
  },
  {
    id: 'al_pokoju',
    name: 'Al. Pokoju',
    district: 'Nowa Huta',
    coordinates: [
      [50.0580, 19.9620], // Rondo Grzegórzeckie
      [50.0610, 19.9900], // M1 Centrum Handlowe
      [50.0680, 20.0150], // Rondo Czyżyńskie
    ],
    morningPeak: 85,
    afternoonPeak: 88,
    offPeak: 32,
    lengthKm: 4.5,
    speedLimit: 60,
  },
  {
    id: 'kotlarska_grzegorzecka',
    name: 'ul. Kotlarska / Most Kotlarski / Grzegórzecka',
    district: 'Centrum',
    coordinates: [
      [50.0560, 19.9535], // Hala Targowa
      [50.0580, 19.9620], // Rondo Grzegórzeckie
      [50.0515, 19.9620], // Most Kotlarski
      [50.0480, 19.9650], // Zabłocie / Klimeckiego
    ],
    morningPeak: 92,
    afternoonPeak: 94,
    offPeak: 40,
    lengthKm: 1.8,
    speedLimit: 50,
  },

  // ==========================================
  // 6. ZACHÓD (Czarnowiejska / Armii Krajowej / Ruczaj)
  // ==========================================
  {
    id: 'czarnowiejska_nawojki',
    name: 'ul. Czarnowiejska / Nawojki',
    district: 'Zachód',
    coordinates: [
      [50.0665, 19.9245], // Plac Inwalidów
      [50.0675, 19.9130], // Miasteczko Studenckie AGH
      [50.0690, 19.9000], // Armii Krajowej
    ],
    morningPeak: 92,
    afternoonPeak: 95,
    offPeak: 45,
    lengthKm: 1.9,
    speedLimit: 50,
  },
  {
    id: 'armii_krajowej_radzikowskiego',
    name: 'ul. Armii Krajowej / Radzikowskiego',
    district: 'Zachód',
    coordinates: [
      [50.0690, 19.9000],
      [50.0820, 19.8920], // Bronowice Wiadukt
      [50.0890, 19.8950], // Rondo Ofiar Katynia
    ],
    morningPeak: 89,
    afternoonPeak: 92,
    offPeak: 35,
    lengthKm: 3.0,
    speedLimit: 60,
  },
  {
    id: 'kapelanka_ruczaj',
    name: 'ul. Kapelanka / Grota-Roweckiego (Kampus UJ)',
    district: 'Zachód',
    coordinates: [
      [50.0450, 19.9300], // Rondo Grunwaldzkie
      [50.0350, 19.9150], // Kobierzyńska
      [50.0260, 19.9000], // Kampus UJ Ruczaj
      [50.0150, 19.8880], // Czerwone Maki P+R
    ],
    morningPeak: 86,
    afternoonPeak: 90,
    offPeak: 32,
    lengthKm: 4.8,
    speedLimit: 60,
  },
]

// Kluczowe punkty i węzły komunikacyjne dla całego Krakowa
// Zawiera exact match "ul. Rynek 1" z Figmy!
export const krakowKeyPoints: TrafficPoint[] = [
  {
    id: 'rynek-1',
    name: 'ul. Rynek 1',
    district: 'Stare Miasto',
    lat: 50.0617,
    lng: 19.9373,
    description: 'Rynek Główny – historyczne serce Krakowa, strefa piesza A/B',
    congestionBase: 20,
  },
  {
    id: 'rondo-mogilskie',
    name: 'Rondo Mogilskie',
    district: 'Śródmieście',
    lat: 50.0665,
    lng: 19.9600,
    description: 'Dwupoziomowy główny węzeł komunikacyjny Krakowa (Mogilska / Lubicz / Powstania Warszawskiego)',
    congestionBase: 92,
  },
  {
    id: 'rondo-grzegorzeckie',
    name: 'Rondo Grzegórzeckie',
    district: 'Śródmieście / Grzegórzki',
    lat: 50.0580,
    lng: 19.9620,
    description: 'Połączenie Al. Pokoju, Kotlarskiej (Most Kotlarski) i Grzegórzeckiej',
    congestionBase: 88,
  },
  {
    id: 'rondo-matecznego',
    name: 'Rondo Matecznego',
    district: 'Podgórze',
    lat: 50.0355,
    lng: 19.9420,
    description: 'Kluczowe wąskie gardło na południu: zbieg Konopnickiej, Kamieńskiego, Zakopiańskiej i Kalwaryjskiej',
    congestionBase: 97,
  },
  {
    id: 'rondo-grunwaldzkie',
    name: 'Rondo Grunwaldzkie',
    district: 'Dębniki / Stare Miasto',
    lat: 50.0485,
    lng: 19.9325,
    description: 'Wjazd na Most Grunwaldzki, centrum kongresowe ICE Kraków, Kapelanka i Dietla',
    congestionBase: 85,
  },
  {
    id: 'rondo-ofiar-katynia',
    name: 'Rondo Ofiar Katynia',
    district: 'Krowodrza / Bronowice',
    lat: 50.0890,
    lng: 19.8950,
    description: 'Trzypoziomowy węzeł wlotowy z A4, DK94 (Olkusz) i wylot na lotnisko Balice',
    congestionBase: 82,
  },
  {
    id: 'plac-centralny',
    name: 'Plac Centralny im. Ronalda Reagana',
    district: 'Nowa Huta',
    lat: 50.0715,
    lng: 20.0380,
    description: 'Centrum architektoniczne i komunikacyjne Nowej Huty (Al. Jana Pawła II / Solidarności / Andersa)',
    congestionBase: 65,
  },
  {
    id: 'most-debnicki',
    name: 'Most Dębnicki (Jubilat)',
    district: 'Śródmieście / Dębniki',
    lat: 50.0525,
    lng: 19.9285,
    description: 'Najbardziej obciążona przeprawa mostowa w Krakowie w ciągu Alej Trzech Wieszczów',
    congestionBase: 98,
  },
  {
    id: 'nowy-kleparz',
    name: 'Nowy Kleparz / Długa',
    district: 'Krowodrza',
    lat: 50.0735,
    lng: 19.9330,
    description: 'Wjazd do centrum od północy i wylotu na Warszawę (Al. Słowackiego / Prądnicka / Długa)',
    congestionBase: 89,
  },
  {
    id: 'wezel-wielicki',
    name: 'Węzeł Wielicki (A4 / Wielicka)',
    district: 'Bieżanów-Prokocim',
    lat: 50.0120,
    lng: 20.0150,
    description: 'Południowo-wschodni wlot do Krakowa z autostrady A4 i drogi krajowej 94',
    congestionBase: 84,
  },
]

export interface CongestionData {
  percent: number // 0-100%
  status: 'low' | 'medium' | 'high'
  color: string
  speedKmH: number
  delayMinutes: number
}

/**
 * Wylicza natężenie ruchu dla danej ulicy w zależności od godziny doby (0-23)
 */
export function getStreetCongestionForHour(street: TrafficStreet, hour: number): CongestionData {
  let percent = street.offPeak

  // Szczyt poranny (07:00 - 09:30)
  if (hour >= 7 && hour <= 9) {
    const factor = hour === 8 ? 1.0 : (hour === 7 ? 0.85 : 0.9)
    percent = Math.round(street.morningPeak * factor)
  }
  // Szczyt popołudniowy (15:00 - 18:30)
  else if (hour >= 15 && hour <= 18) {
    const factor = hour === 17 ? 1.0 : (hour === 16 ? 0.95 : 0.85)
    percent = Math.round(street.afternoonPeak * factor)
  }
  // Pora nocna (22:00 - 05:00)
  else if (hour >= 22 || hour <= 5) {
    percent = Math.max(5, Math.round(street.offPeak * 0.25))
  }
  // Godziny dzienne (10:00 - 14:00)
  else {
    percent = Math.round(street.offPeak * 1.05)
  }

  // Ograniczenie 0-100%
  percent = Math.min(100, Math.max(5, percent))

  // Exact Figma tokens:
  // Green (#37dd00) dla < 40%, Warning/Orange (#f29a01) dla 40-70%, Error/Red (#ec1f00) dla > 70%
  let status: 'low' | 'medium' | 'high' = 'low'
  let color = '#37dd00' // Success 500

  if (percent > 70) {
    status = 'high'
    color = '#ec1f00' // Error 500
  } else if (percent > 40) {
    status = 'medium'
    color = '#f29a01' // Warning 500
  }

  const speedLimit = street.speedLimit || 50
  const speedKmH = Math.max(5, Math.round(speedLimit * (1 - (percent / 100) * 0.85)))
  const standardMinutes = (street.lengthKm / speedLimit) * 60
  const actualMinutes = (street.lengthKm / speedKmH) * 60
  const delayMinutes = Math.max(0, Math.round(actualMinutes - standardMinutes))

  return {
    percent,
    status,
    color,
    speedKmH,
    delayMinutes,
  }
}

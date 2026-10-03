/**
 * TomTom Traffic API Service for Kraków
 * Handles live traffic flow tiles, incident tiles, and flow segment queries.
 */

// Klucz API domyślny lub pobierany z localStorage / zmiennych środowiskowych
const STORAGE_KEY = 'tomtom_api_key'

export function getStoredApiKey(): string {
  const envKey = import.meta.env.VITE_TOMTOM_API_KEY as string | undefined
  if (envKey && envKey.trim().length > 0) {
    return envKey.trim()
  }
  const local = localStorage.getItem(STORAGE_KEY)
  return local ? local.trim() : ''
}

export function saveApiKey(key: string): void {
  if (key && key.trim().length > 0) {
    localStorage.setItem(STORAGE_KEY, key.trim())
  } else {
    localStorage.removeItem(STORAGE_KEY)
  }
}

/**
 * Zwraca URL do warstwy kafelków Traffic Flow TomTom (względna prędkość - zielony/pomarańczowy/czerwony)
 */
export function getTrafficFlowTileUrl(apiKey: string): string {
  // style: 'relative' lub 'relative0' (pokazuje zatory względem prędkości swobodnego ruchu)
  return `https://api.tomtom.com/traffic/map/4/tile/flow/relative/{z}/{x}/{y}.png?key=${apiKey}`
}

/**
 * Zwraca URL do warstwy incydentów TomTom (wypadki, roboty drogowe, zamknięte pasy)
 */
export function getTrafficIncidentsTileUrl(apiKey: string): string {
  return `https://api.tomtom.com/traffic/map/4/tile/incidents/s3/{z}/{x}/{y}.png?key=${apiKey}`
}

export interface TomTomSegmentData {
  streetName?: string
  currentSpeed: number
  freeFlowSpeed: number
  currentTravelTime: number
  freeFlowTravelTime: number
  delaySeconds: number
  confidence: number
  roadClosure: boolean
  congestionLevel: number // 0-100%
  status: 'low' | 'medium' | 'high'
  color: string
  coordinates?: [number, number][]
}

/**
 * Odpytuje TomTom Flow Segment Data dla dowolnego punktu [lat, lng] w Krakowie
 */
export async function fetchLiveFlowSegment(
  lat: number,
  lng: number,
  apiKey: string
): Promise<TomTomSegmentData | null> {
  if (!apiKey) return null

  try {
    // TomTom Flow Segment Data v4
    const url = `https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?point=${lat},${lng}&unit=KMPH&key=${apiKey}`
    const response = await fetch(url)
    if (!response.ok) {
      console.warn('TomTom Flow Segment API error:', response.status, response.statusText)
      return null
    }

    const data = await response.json()
    const flow = data.flowSegmentData
    if (!flow) return null

    const currentSpeed = Math.round(flow.currentSpeed ?? 0)
    const freeFlowSpeed = Math.max(1, Math.round(flow.freeFlowSpeed ?? 50))
    const currentTravelTime = Math.round(flow.currentTravelTime ?? 0)
    const freeFlowTravelTime = Math.round(flow.freeFlowTravelTime ?? 0)
    const delaySeconds = Math.max(0, currentTravelTime - freeFlowTravelTime)

    // Wyliczenie poziomu zakorkowania (0 - 100%)
    let congestionLevel = Math.round((1 - currentSpeed / freeFlowSpeed) * 100)
    if (congestionLevel < 0) congestionLevel = 0
    if (congestionLevel > 100) congestionLevel = 100
    if (flow.roadClosure) congestionLevel = 100

    let status: 'low' | 'medium' | 'high' = 'low'
    let color = '#37dd00' // Zielony (Success 500)

    if (congestionLevel > 65 || flow.roadClosure) {
      status = 'high'
      color = '#ec1f00' // Czerwony (Error 500)
    } else if (congestionLevel > 30) {
      status = 'medium'
      color = '#f29a01' // Pomarańczowy (Warning 500)
    }

    // Odczytanie współrzędnych segmentu, jeśli API je zwróciło
    let coords: [number, number][] | undefined = undefined
    if (flow.coordinates && flow.coordinates.coordinate) {
      coords = flow.coordinates.coordinate.map(
        (c: { latitude: number; longitude: number }) => [c.latitude, c.longitude] as [number, number]
      )
    }

    return {
      currentSpeed,
      freeFlowSpeed,
      currentTravelTime,
      freeFlowTravelTime,
      delaySeconds,
      confidence: flow.confidence ?? 1,
      roadClosure: flow.roadClosure ?? false,
      congestionLevel,
      status,
      color,
      coordinates: coords,
    }
  } catch (err) {
    console.error('Error fetching TomTom flow segment:', err)
    return null
  }
}

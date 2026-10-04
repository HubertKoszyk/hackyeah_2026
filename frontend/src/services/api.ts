import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8001',
  timeout: 8000,
})

export interface ParkingItem {
  id: number
  name: string
  lat: number
  lng: number
  totalSpots: number
  freeSpots: number
  status: 'available' | 'almost_full' | 'full'
}

export const fetchParkingSpots = async (): Promise<ParkingItem[]> => {
  const response = await api.get<ParkingItem[]>('/parking/get/all/')
  return response.data
}

export interface RoadRestriction {
  id: number
  title: string
  kind: 'roadwork' | 'event' | 'accident' | 'closure'
  kind_label: string
  organization: string
  description: string
  detour: string
  status: 'active' | 'planned' | 'finished'
  start: { lat: number; lng: number }
  end: { lat: number; lng: number }
  start_at: string
  end_at: string
  conflicts: { id: number; title: string }[]
  nearby_parkings: { id: number; name: string; distance_m: number }[]
}

export const fetchRoadworks = async (): Promise<RoadRestriction[]> => {
  const response = await api.get<RoadRestriction[]>('/roadworks/', {
    params: { hide_finished: 1 },
  })
  return response.data
}

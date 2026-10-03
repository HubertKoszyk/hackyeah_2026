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

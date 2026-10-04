import type { RoadRestriction } from './api'
import type { TrafficStreet, CongestionData } from '../data/krakowTrafficData'

// Promień (m), w którym ograniczenie wpływa na ruch na ulicy
export const IMPACT_RADIUS_M = 250
// Poniżej tej odległości ulica jest uznawana za bezpośrednio dotkniętą
const DIRECT_HIT_M = 40

// Ile punktów procentowych natężenia dokłada dany rodzaj ograniczenia (przy trafieniu bezpośrednim)
const KIND_PENALTY: Record<RoadRestriction['kind'], number> = {
  closure: 60,
  accident: 45,
  roadwork: 30,
  event: 35,
}

export interface StreetImpact {
  extraPercent: number
  closed: boolean
  causes: RoadRestriction[]
}

type LatLng = [number, number]

// Rzutowanie lokalne (equirectangular) – wystarcza w skali miasta
const toXY = ([lat, lng]: LatLng, refLat: number): [number, number] => {
  const k = 111320
  return [lng * k * Math.cos((refLat * Math.PI) / 180), lat * k]
}

function pointToSegmentM(p: LatLng, a: LatLng, b: LatLng): number {
  const refLat = p[0]
  const [px, py] = toXY(p, refLat)
  const [ax, ay] = toXY(a, refLat)
  const [bx, by] = toXY(b, refLat)
  const dx = bx - ax
  const dy = by - ay
  const len2 = dx * dx + dy * dy
  let t = len2 === 0 ? 0 : ((px - ax) * dx + (py - ay) * dy) / len2
  t = Math.max(0, Math.min(1, t))
  return Math.hypot(px - (ax + t * dx), py - (ay + t * dy))
}

// Minimalna odległość polilinii ulicy od odcinka ograniczenia (próbkowanie co ~1/10 odcinka)
function streetDistanceM(coords: LatLng[], a: LatLng, b: LatLng): number {
  let min = Infinity
  for (let i = 0; i < coords.length - 1; i++) {
    const p0 = coords[i]!
    const p1 = coords[i + 1]!
    for (let s = 0; s <= 10; s++) {
      const t = s / 10
      const p: LatLng = [p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t]
      min = Math.min(min, pointToSegmentM(p, a, b))
    }
  }
  return min
}

export function getStreetImpact(street: TrafficStreet, restrictions: RoadRestriction[]): StreetImpact {
  const impact: StreetImpact = { extraPercent: 0, closed: false, causes: [] }

  for (const r of restrictions) {
    // Wpływ na ruch mają tylko trwające ograniczenia
    if (r.status !== 'active') continue

    const d = streetDistanceM(
      street.coordinates as LatLng[],
      [r.start.lat, r.start.lng],
      [r.end.lat, r.end.lng],
    )
    if (d > IMPACT_RADIUS_M) continue

    const falloff =
      d <= DIRECT_HIT_M ? 1 : 1 - (d - DIRECT_HIT_M) / (IMPACT_RADIUS_M - DIRECT_HIT_M)
    impact.extraPercent += KIND_PENALTY[r.kind] * falloff
    if (r.kind === 'closure' && d <= DIRECT_HIT_M) impact.closed = true
    impact.causes.push(r)
  }

  impact.extraPercent = Math.round(impact.extraPercent)
  return impact
}

// Nakłada wpływ ograniczeń na bazowe natężenie ruchu z symulacji godzinowej
export function applyImpact(base: CongestionData, impact: StreetImpact, speedLimit: number, lengthKm: number): CongestionData {
  if (impact.extraPercent <= 0) return base

  const percent = impact.closed ? 100 : Math.min(100, base.percent + impact.extraPercent)
  let status: CongestionData['status'] = 'low'
  let color = '#37dd00'
  if (percent > 70) {
    status = 'high'
    color = '#ec1f00'
  } else if (percent > 40) {
    status = 'medium'
    color = '#f29a01'
  }

  const speedKmH = Math.max(5, Math.round(speedLimit * (1 - (percent / 100) * 0.85)))
  const standardMinutes = (lengthKm / speedLimit) * 60
  const actualMinutes = (lengthKm / speedKmH) * 60
  const delayMinutes = Math.max(0, Math.round(actualMinutes - standardMinutes))

  return { percent, status, color, speedKmH, delayMinutes }
}

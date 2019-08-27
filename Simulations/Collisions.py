class Vector:
    def __init__(self, x_component, y_component):
        self.x = x_component
        self.y = y_component

    def perpendicular(self):
        return Vector(self.y, -1 * self.x)

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

def VectorAdd(V1, V2):
    return Vector(V1.x + V2.x, V1.y + V2.y)

def VectorSubtract(V1, V2):
    return Vector(V1.x - V2.x, V1.y - V2.y)

def ScalarMultiply(v, k):
    return Vector(k * v.x, k * v.y)

def UnitVector(v):
    return ScalarMultiply(v, float(1) / float(v.magnitude()))

def Dot(V1, V2):
    return V1.x * V2.x + V1.y * V2.y

def Collision(m1, m2, x1, x2, v1, v2, e):
    r = UnitVector(VectorSubtract(x2, x1))
    s = UnitVector(r.perpendicular())

    if Dot(v1, r) - Dot(v2, r) <= 0:
        return v1
    else:
        perp = Dot(v1, s)
        para = float((m1 - m2 * e) * Dot(v1, r) + (m2 + m2 * e) * Dot(v2, r)) / float(m1 + m2)

        return VectorAdd( ScalarMultiply(r, para), ScalarMultiply(s, perp))


    
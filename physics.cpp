#include "physics.h"
#include <cmath>

bool check_collision(float x1, float y1, float r1, float x2, float y2, float r2) {
    float dx = x1 - x2;
    float dy = y1 - y2;
    float distance = std::sqrt(dx * dx + dy * dy);
    return distance <= (r1 + r2);
}
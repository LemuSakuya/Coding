#include <bits/stdc++.h>
using namespace std;

struct P { double x, y; };
double dist2(P a, P b){ return (a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y); }
struct Circle { P c; double r2; };

bool inside(Circle C, P p) { return dist2(C.c, p) <= C.r2 + 1e-10; }

Circle from2(P a, P b) {
    P c = {(a.x+b.x)/2, (a.y+b.y)/2};
    return {c, dist2(c, a)};
}

Circle from3(P a, P b, P c) {
    double ax=a.x, ay=a.y, bx=b.x, by=b.y, cx=c.x, cy=c.y;
    double d = 2*(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by));
    if (fabs(d) < 1e-18) {
        Circle C1 = from2(a,b), C2 = from2(a,c), C3 = from2(b,c);
        Circle best = C1;
        if (C2.r2 > best.r2) best = C2;
        if (C3.r2 > best.r2) best = C3;
        return best;
    }
    double ux = ((ax*ax+ay*ay)*(by-cy) + (bx*bx+by*by)*(cy-ay) + (cx*cx+cy*cy)*(ay-by))/d;
    double uy = ((ax*ax+ay*ay)*(cx-bx) + (bx*bx+by*by)*(ax-cx) + (cx*cx+cy*cy)*(bx-ax))/d;
    P cen = {ux, uy};
    return {cen, dist2(cen, a)};
}

Circle welzl(vector<P> pts) {
    mt19937 rng(20260510);
    shuffle(pts.begin(), pts.end(), rng);
    int n = pts.size();
    Circle C = {{0,0}, 0};
    for (int i = 0; i < n; i++) {
        if (inside(C, pts[i])) continue;
        C = {pts[i], 0};
        for (int j = 0; j < i; j++) {
            if (inside(C, pts[j])) continue;
            C = from2(pts[i], pts[j]);
            for (int k = 0; k < j; k++) {
                if (inside(C, pts[k])) continue;
                C = from3(pts[i], pts[j], pts[k]);
            }
        }
    }
    return C;
}

int main() {
    int n;
    scanf("%d", &n);
    vector<int> L(n+1), R(n+1);
    for (int i = 1; i <= n; i++) scanf("%d %d", &L[i], &R[i]);

    const double S = sqrt(3.0) / 2.0;
    vector<P> ctr(n+1);
    ctr[1] = {0.0, 0.0};
    for (int i = 1; i <= n; i++) {
        if (L[i] != -1) ctr[L[i]] = {ctr[i].x - S, ctr[i].y - 1.5};
        if (R[i] != -1) ctr[R[i]] = {ctr[i].x + S, ctr[i].y - 1.5};
    }

    double dx[6] = { S, 0.0, -S, -S,  0.0,  S};
    double dy[6] = { 0.5, 1.0, 0.5, -0.5, -1.0, -0.5};
    vector<P> verts;
    verts.reserve(6 * n);
    for (int i = 1; i <= n; i++)
        for (int k = 0; k < 6; k++)
            verts.push_back({ctr[i].x + dx[k], ctr[i].y + dy[k]});

    Circle C = welzl(verts);
    printf("%.4f\n", C.r2);
    return 0;
}

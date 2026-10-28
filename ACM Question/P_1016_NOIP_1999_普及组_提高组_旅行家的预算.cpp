#include <bits/stdc++.h>
using namespace std;

using ld = long double;
const ld eps = 1e-10L;

struct stop {
    ld d, p;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ld s, c, l, p0;
    int n;
    cin >> s >> c >> l >> p0 >> n;

    vector<stop> v = {{0, p0}, {s, 0}};

    while (n--) {
        ld d, p;
        cin >> d >> p;
        v.push_back({d, p});
    }

    sort (v.begin(), v.end(), [](const stop &a, const stop &b) {
        if (a.d != b.d) return a.d < b.d;
        return a.p < b.p;
    });

    vector<stop> a;
    for (auto x : v) {
        if (!a.empty() && fabsl(a.back().d - x.d) < eps) {
            a.back().p = min(a.back().p, x.p);
        } else {
            a.push_back(x);
        }
    }

    if (s < eps) {
        cout << "0.00" << endl;
        return 0;
    }

    ld to = c * l;
    ld oil = 0, cost = 0;
    int i = 0;

    while (i + 1 < (int)a.size()) {
        int er = -1, est = -1;

        for (int j = i + 1; j < (int)a.size(); j++) {
            if (a[j].d - a[i].d > to + eps) {
                break;
            }

            if (er == -1 && a[j].p + eps < a[i].p) {
                er = j;
            }

            if (est == -1 || a[j].p < a[est].p) {
                est = j;
            }
        }

        if (est == -1) {
            cout << "No Solution" << endl;
            return 0;
        }

        int j = er == -1 ? est : er;
        ld need = er == -1 ? c : (a[j].d - a[i].d) / l;

        if (oil + eps < need) {
            cost += (need - oil) * a[i].p;
            oil = need;
        }

        oil = max((ld)0, oil - (a[j].d - a[i].d) / l);
        i = j;
    }

    cout << fixed << setprecision(2) << cost << endl;
    return 0;
}
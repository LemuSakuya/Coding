// Fill gen(), brute(), solve() for a specific problem.
for (int tc = 1; tc <= 10000; ++tc) {
    auto data = gen(tc);
    auto a = brute(data);
    auto b = solve(data);
    if (a != b) {
        cerr << "Wrong answer on seed " << tc << '
';
        print(data);
        cerr << "brute = " << a << " solve = " << b << '
';
        break;
    }
}

#include <algorithm>
#include <array>
#include <cassert>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <vector>

struct SignedComponents {
    std::vector<int> parent, parity, rank, zero;
    explicit SignedComponents(int n) : parent(n), parity(n), rank(n), zero(n) {
        std::iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        if (parent[x] != x) {
            int p = parent[x];
            parent[x] = find(p);
            parity[x] ^= parity[p];
        }
        return parent[x];
    }
    void opposite(int x, int y) {
        int a = find(x), b = find(y);
        int difference = parity[x] ^ parity[y] ^ 1;
        if (a == b) {
            if (difference) zero[a] = 1;
            return;
        }
        if (rank[a] < rank[b]) std::swap(a, b);
        parent[b] = a;
        parity[b] = difference;
        zero[a] |= zero[b];
        if (rank[a] == rank[b]) ++rank[a];
    }
    std::vector<int> profile() {
        std::vector<int> out(parent.size());
        for (int i = 0; i < (int)out.size(); ++i) {
            int r = find(i);
            out[i] = zero[r] ? 0 : (parity[i] ? -1 : 1) * (r + 1);
        }
        return out;
    }
};

std::vector<int> normalize(const std::vector<int>& p) {
    std::map<int, int> names;
    std::vector<int> out;
    for (int x : p) {
        if (!x) { out.push_back(0); continue; }
        int key = std::abs(x), sign = x < 0 ? -1 : 1;
        if (!names.count(key)) names[key] = sign * ((int)names.size() + 1);
        out.push_back(sign * names[key]);
    }
    return out;
}

struct Record {
    std::array<int, 8> poses;
    std::vector<int> profile, contacts;
    int templates = 0;
};

int main(int argc, char** argv) {
    assert(argc == 3);
    std::ifstream in(argv[1]);
    int ports, count;
    in >> ports >> count;
    std::vector<std::vector<std::pair<int, int>>> pairs(count);
    for (auto& row : pairs) {
        int size; in >> size;
        for (int k = 0; k < size; ++k) {
            int a, b; in >> a >> b; row.emplace_back(a, b);
        }
    }
    std::array<std::array<int, 24>, 24> seeds;
    for (auto& row : seeds) for (auto& x : row) in >> x;
    std::vector<std::array<std::array<int, 24>, 24>> next(count);
    for (auto& matrix : next) for (auto& row : matrix) for (auto& x : row) in >> x;
    std::vector<std::vector<int>> symmetries(3, std::vector<int>(ports));
    for (auto& row : symmetries) for (auto& x : row) in >> x;
    assert(in.good());
    std::map<std::vector<int>, Record> profiles;
    std::map<int, int> histogram;
    int flat = 0;
    for (int code = 0; code < 6561; ++code) {
        int number = code;
        std::array<int, 8> poses, selected;
        for (int j = 0; j < 8; ++j) {
            poses[j] = number % 3;
            number /= 3;
            selected[j] = 3 * j + poses[j];
        }
        std::vector<int> contacts;
        std::vector<bool> seen(count);
        auto add = [&](int t) {
            if (t >= 0 && !seen[t]) { seen[t] = true; contacts.push_back(t); }
        };
        for (int j : selected) for (int k : selected) add(seeds[j][k]);
        for (size_t i = 0; i < contacts.size(); ++i)
            for (int j : selected) for (int k : selected) add(next[contacts[i]][j][k]);
        SignedComponents constraints(ports);
        for (int t : contacts) for (auto [a, b] : pairs[t]) constraints.opposite(a, b);
        auto profile = normalize(constraints.profile());
        int components = 0;
        for (int x : profile) components = std::max(components, std::abs(x));
        ++histogram[components];
        if (!components) ++flat;
        auto canonical = profile;
        for (const auto& permutation : symmetries) {
            std::vector<int> moved(ports);
            for (int i = 0; i < ports; ++i) moved[permutation[i]] = profile[i];
            canonical = std::min(canonical, normalize(moved));
        }
        auto [it, inserted] = profiles.try_emplace(canonical);
        if (inserted) {
            it->second.poses = poses;
            it->second.profile = profile;
            std::sort(contacts.begin(), contacts.end());
            it->second.contacts = contacts;
        }
        ++it->second.templates;
        if ((code + 1) % 1000 == 0)
            std::cerr << "Templates " << code + 1 << "/6561, profile classes " << profiles.size() << '\n';
    }
    std::ofstream out(argv[2]);
    auto array = [&](const auto& values) {
        out << '['; bool first = true;
        for (int x : values) { if (!first) out << ','; first = false; out << x; }
        out << ']';
    };
    out << "{\"templates_enumerated\":6561,\"flat_only_templates\":" << flat
        << ",\"profile_classes\":" << profiles.size() << ",\"component_histogram\":{";
    bool first = true;
    for (auto [n, amount] : histogram) {
        if (!first) out << ','; first = false;
        out << '\"' << n << "\":" << amount;
    }
    out << "},\"profiles\":[";
    first = true;
    for (const auto& [key, record] : profiles) {
        if (!first) out << ','; first = false;
        out << "{\"template\":"; array(record.poses);
        out << ",\"template_count\":" << record.templates << ",\"labels\":"; array(record.profile);
        out << ",\"closed_contact_types\":"; array(record.contacts);
        out << '}';
    }
    out << "]}\n";
}

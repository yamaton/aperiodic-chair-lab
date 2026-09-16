// Exact rooted connected-cluster enumeration; driven and checked through uv.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>

using Vec = std::array<int, 3>;
struct Tile { Vec p; int direction; };
struct Rotation { Vec axes, signs; };
using ShapeKey = std::array<uint32_t, 8>;

std::vector<Tile> tiles;
std::vector<std::vector<int>> adjacent;
std::vector<Rotation> rotations;
std::vector<int> targets, status, dense;
std::vector<std::vector<std::vector<int>>> matching_rotations;
std::map<ShapeKey, uint64_t> survivors;
std::map<size_t, std::array<int, 8>> rejection_examples;
std::array<int, 8> cluster;
std::vector<uint64_t> rejected_at;
uint64_t examined = 0, accepted = 0, nodes = 0;
int radius, width, cluster_size;
double seconds;
bool complete = true;
std::chrono::steady_clock::time_point started;

double elapsed() {
    return std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
}

Vec rotate(const Vec &p, int r) {
    Vec q;
    for (int k = 0; k < 3; ++k) q[k] = rotations[r].signs[k] * p[rotations[r].axes[k]];
    return q;
}

int direction_after(int d, int r) {
    Vec p;
    for (int k = 0; k < 3; ++k) p[k] = (d & (1 << k)) ? 1 : -1;
    Vec q = rotate(p, r);
    return (q[0] > 0) + 2 * (q[1] > 0) + 4 * (q[2] > 0);
}

int at(const Vec &p) {
    for (int v : p) if (v < -radius || v > radius) return -1;
    return dense[((p[0] + radius) * width + p[1] + radius) * width + p[2] + radius];
}

void inspect() {
    ++examined;
    std::array<std::array<Vec, 8>, 24> transformed;
    std::array<std::array<int, 8>, 24> directions;
    for (int r = 0; r < 24; ++r)
        for (int j = 0; j < cluster_size; ++j) {
            transformed[r][j] = rotate(tiles[cluster[j]].p, r);
            directions[r][j] = direction_after(tiles[cluster[j]].direction, r);
        }
    for (size_t t = 0; t < targets.size(); ++t) {
        const Tile &target = tiles[targets[t]];
        bool occurs = false;
        for (int j = 0; j < cluster_size && !occurs; ++j) {
            for (int r : matching_rotations[tiles[cluster[j]].direction][target.direction]) {
                Vec shift;
                for (int k = 0; k < 3; ++k) shift[k] = target.p[k] - transformed[r][j][k];
                bool good = true;
                for (int i = 0; i < cluster_size; ++i) {
                    if (i == j) continue;
                    Vec p;
                    for (int k = 0; k < 3; ++k) p[k] = transformed[r][i][k] + shift[k];
                    int found = at(p);
                    if (found < 0 || tiles[found].direction != directions[r][i]) {
                        good = false;
                        break;
                    }
                }
                if (good) { occurs = true; break; }
            }
        }
        if (!occurs) {
            ++rejected_at[t];
            if (!rejection_examples.count(t)) rejection_examples[t] = cluster;
            return;
        }
    }
    ++accepted;
    ShapeKey best;
    best.fill(UINT32_MAX);
    for (int r = 0; r < 24; ++r) {
        Vec lower = transformed[r][0];
        for (int i = 1; i < cluster_size; ++i)
            for (int k = 0; k < 3; ++k) lower[k] = std::min(lower[k], transformed[r][i][k]);
        ShapeKey key;
        key.fill(UINT32_MAX);
        for (int i = 0; i < cluster_size; ++i) {
            Vec p;
            for (int k = 0; k < 3; ++k) {
                p[k] = transformed[r][i][k] - lower[k];
                if (p[k] < 0 || p[k] >= 32) throw std::runtime_error("shape encoding bound");
            }
            key[i] = ((p[0] * 32 + p[1]) * 32 + p[2]) * 8 + directions[r][i];
        }
        std::sort(key.begin(), key.begin() + cluster_size);
        best = std::min(best, key);
    }
    ++survivors[best];
}

// Status: 0 unseen, 1 in cluster, 2 frontier, 3 excluded by an earlier sibling.
// Each call restores the status array to its entry state.
void grow(int size, std::vector<int> frontier) {
    ++nodes;
    if ((nodes % 10000) == 0 && elapsed() > seconds) {
        complete = false;
        return;
    }
    std::vector<int> processed;
    while (!frontier.empty() && complete) {
        int v = frontier.back();
        frontier.pop_back();
        status[v] = 1;
        cluster[size] = v;
        if (size + 1 == cluster_size) {
            inspect();
            if (examined % 250000 == 0)
                std::cerr << examined << " rooted clusters, " << survivors.size()
                          << " surviving shapes, " << elapsed() << " seconds\n";
        } else {
            auto next = frontier;
            std::vector<int> added;
            for (int w : adjacent[v]) if (status[w] == 0) {
                status[w] = 2;
                next.push_back(w);
                added.push_back(w);
            }
            grow(size + 1, std::move(next));
            for (int w : added) status[w] = 0;
        }
        status[v] = 3;
        processed.push_back(v);
    }
    for (int v : processed) status[v] = 2;
}

int main(int argc, char **argv) {
    if (argc != 3) return 2;
    std::ifstream input(argv[1]);
    int count, root, target_count;
    input >> count >> radius >> root >> cluster_size >> seconds >> target_count;
    if (!input || cluster_size < 2 || cluster_size > 8) return 3;
    width = 2 * radius + 1;
    dense.assign(width * width * width, -1);
    tiles.resize(count);
    adjacent.resize(count);
    status.assign(count, 0);
    for (int i = 0; i < count; ++i) {
        auto &tile = tiles[i];
        input >> tile.p[0] >> tile.p[1] >> tile.p[2] >> tile.direction;
        int slot = ((tile.p[0] + radius) * width + tile.p[1] + radius) * width + tile.p[2] + radius;
        dense[slot] = i;
        int degree;
        input >> degree;
        adjacent[i].resize(degree);
        for (int &j : adjacent[i]) input >> j;
    }
    rotations.resize(24);
    for (auto &r : rotations) {
        for (int &v : r.axes) input >> v;
        for (int &v : r.signs) input >> v;
    }
    targets.resize(target_count);
    for (int &target : targets) input >> target;
    if (!input) return 4;
    rejected_at.assign(target_count, 0);
    matching_rotations.resize(8, std::vector<std::vector<int>>(8));
    for (int a = 0; a < 8; ++a)
        for (int r = 0; r < 24; ++r) matching_rotations[a][direction_after(a, r)].push_back(r);
    cluster[0] = root;
    status[root] = 1;
    for (int v : adjacent[root]) status[v] = 2;
    started = std::chrono::steady_clock::now();
    grow(1, adjacent[root]);
    std::ofstream out(argv[2]);
    out << "{\"enumeration_complete\":" << (complete ? "true" : "false")
        << ",\"rooted_clusters_examined\":" << examined << ",\"accepted_rooted_clusters\":" << accepted
        << ",\"surviving_shape_classes\":" << survivors.size() << ",\"elapsed_seconds\":" << elapsed()
        << ",\"rejected_at_target\":[";
    for (size_t i = 0; i < rejected_at.size(); ++i) out << (i ? "," : "") << rejected_at[i];
    out << "],\"shapes\":[";
    bool first = true;
    for (const auto &[key, multiplicity] : survivors) {
        if (!first) out << ',';
        first = false;
        out << "{\"anchor_occurrences\":" << multiplicity << ",\"chairs\":[";
        for (int i = 0; i < cluster_size; ++i) {
            if (i) out << ',';
            uint32_t v = key[i];
            int d = v % 8; v /= 8;
            int z = v % 32; v /= 32;
            int y = v % 32; int x = v / 32;
            out << "[[" << x << ',' << y << ',' << z << "],["
                << ((d & 1) ? 1 : -1) << ',' << ((d & 2) ? 1 : -1) << ',' << ((d & 4) ? 1 : -1) << "]]";
        }
        out << "]}";
    }
    out << "],\"rejection_examples\":[";
    first = true;
    for (const auto &[t, ids] : rejection_examples) {
        if (!first) out << ',';
        first = false;
        out << "{\"target\":" << targets[t] << ",\"cluster\":[";
        for (int j = 0; j < cluster_size; ++j) out << (j ? "," : "") << ids[j];
        out << "]}";
    }
    out << "]}\n";
    std::cerr << "Completed=" << complete << ", " << examined << " clusters, "
              << survivors.size() << " surviving shapes, " << elapsed() << " seconds\n";
}

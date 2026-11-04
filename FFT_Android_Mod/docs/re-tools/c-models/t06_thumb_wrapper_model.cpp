// Bounded semantic model of two ARM Thumb call wrappers, NOT a memory allocator.
// The original external callees are replaced with explicit test callbacks.
// This program is a host-side test oracle for conditional forwarding only.
// It does NOT emulate ARM stack layout, exceptions, JNI, malloc or deallocation.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cerrno>
#include <cstring>
#include <limits>

struct Trace {
    std::uint32_t calls = 0;
    std::uint32_t argument = 0;
    std::uint32_t target = 0;
};

static constexpr std::uint32_t kDeleteCallee = 0x002ce07cu;
static constexpr std::uint32_t kAllocCallee = 0x002c99b4u;

static void mocked_delete(std::uint32_t ptr, Trace &state) {
    ++state.calls;
    state.argument = ptr;
    state.target = kDeleteCallee;
}

static std::uint32_t mocked_new(std::uint32_t bytes,
                                std::uint32_t return_value, Trace &state) {
    ++state.calls;
    state.argument = bytes;
    state.target = kAllocCallee;
    return return_value;
}

static void t06_operator_delete_wrapper(std::uint32_t ptr, Trace &state) {
    if (ptr != 0u) {
        mocked_delete(ptr, state);
    }
}

static std::uint32_t t06_operator_new_array_wrapper(
    std::uint32_t size, std::uint32_t mock_return, Trace &state) {
    return mocked_new(size, mock_return, state);
}

static bool parse_u32(const char *value, std::uint32_t &out) {
    if (!value || !*value || value[0] == '-') {
        return false;
    }
    errno = 0;
    char *end = nullptr;
    const unsigned long v = std::strtoul(value, &end, 0);
    if (errno != 0 || end == value || *end != '\0' ||
        v > std::numeric_limits<std::uint32_t>::max()) {
        return false;
    }
    out = static_cast<std::uint32_t>(v);
    return true;
}

int main(int argc, char **argv) {
    if (argc != 4) {
        std::fputs("Usage: t06_model [delete|new_array] <r0> <mock_r0>\n", stderr);
        return 2;
    }
    std::uint32_t r0 = 0;
    std::uint32_t stub_return = 0;
    if (!parse_u32(argv[2], r0) || !parse_u32(argv[3], stub_return)) {
        std::fputs("Invalid uint32_t input\n", stderr);
        return 2;
    }
    Trace trace;
    std::uint32_t result = 0;
    if (std::strcmp(argv[1], "delete") == 0) {
        t06_operator_delete_wrapper(r0, trace);
    } else if (std::strcmp(argv[1], "new_array") == 0) {
        result = t06_operator_new_array_wrapper(r0, stub_return, trace);
    } else {
        std::fputs("Unknown operation\n", stderr);
        return 2;
    }
    std::printf(
        "{\"calls\":%u,\"argument\":%u,\"target\":%u,\"returned_r0\":%u}\n",
        static_cast<unsigned>(trace.calls),
        static_cast<unsigned>(trace.argument),
        static_cast<unsigned>(trace.target),
        static_cast<unsigned>(result));
    return 0;
}

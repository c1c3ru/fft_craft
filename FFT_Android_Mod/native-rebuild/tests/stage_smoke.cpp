// Tests the bounded, independent staged C++ implementation only.
// It does not load the original Android ELF or claim full caller equivalence.
#include <array>
#include <cstddef>
#include <cstdint>
#include <iostream>

extern "C" int fft_b01_named_cpp_method(
    std::uint32_t elf_entry, std::uint8_t* object, std::size_t object_size,
    std::uint32_t argument_r1) noexcept;

struct Case {
    std::uint32_t entry;
    std::size_t offset;
    std::uint32_t expected;
};

int main() {
    constexpr std::array<Case, 7> cases{{
        {0x000b3518u, 0x000u, 0u},
        {0x000b9f7cu, 0x014u, 2u},
        {0x000b9facu, 0x014u, 8u},
        {0x000b9fb8u, 0x014u, 1u},
        {0x000bdb60u, 0x000u, 0u},
        {0x000be1dcu, 0x020u, 0u},
        {0x0028de9cu, 0x304u, 1u},
    }};
    for (const auto& item : cases) {
        std::array<std::uint8_t, 0x400> object{};
        object.fill(0xa5u);
        const auto before = object;
        if (fft_b01_named_cpp_method(
                item.entry, object.data(), object.size(), 0x12345678u) != 0) {
            std::cerr << "Reconstruction rejected valid staged object\n";
            return 1;
        }
        for (std::size_t i = 0; i < object.size(); ++i) {
            const auto expected = i >= item.offset && i < item.offset + 4
                 ? static_cast<std::uint8_t>(
                       (item.expected >> (8u * (i - item.offset))) & 0xffu)
                 : before[i];
            if (object[i] != expected) {
                std::cerr << "Unexpected object write\n";
                return 2;
            }
        }
        if (fft_b01_named_cpp_method(
                item.entry, object.data(), item.offset + 3, 0u) != -1) {
            std::cerr << "Undersized object accepted\n";
            return 3;
        }
    }
    std::array<std::uint8_t, 0x400> object{};
    if (fft_b01_named_cpp_method(
            0x000b3518u, nullptr, object.size(), 0) != -1 ||
        fft_b01_named_cpp_method(
            0xdeadbeefu, object.data(), object.size(), 0) != -2) {
        std::cerr << "Invalid object/method not rejected\n";
        return 4;
    }
    std::cout << "T32_STAGE_CXX_BOUNDARY_SMOKE=PASS\n"
              << "T32_FULL_ANDROID_ENGINE_BUILT=0\n";
    return 0;
}

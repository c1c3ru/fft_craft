// B01: independent, bounds-checked C++ reconstruction of seven 12-byte
// ARM member-function bodies. Class member names/field offsets are hypotheses;
// this is NOT a replacement for validated in-game C++ object definitions.
#include <cstddef>
#include <cstdint>
#include <cstring>

namespace fft_b01 {
struct ObjectView {
    std::uint8_t* data;
    std::size_t size;

    bool store32(std::size_t offset, std::uint32_t value) const noexcept {
        if (!data || offset > size || size - offset < sizeof(value))
            return false;
        // Explicit little-endian access, no unaligned pointer cast or UB.
        for (std::size_t i=0; i<sizeof(value); ++i)
            data[offset+i] = static_cast<std::uint8_t>(value >> (8u*i));
        return true;
    }
};

struct CINPUT_DATA {
    static bool constructor(ObjectView object) noexcept {
        return object.store32(0x000, 0);
    }
};
struct CTHREAD {
    static bool RequestExit(ObjectView object) noexcept {
        return object.store32(0x014, 2);
    }
    static bool RequestSuspend(ObjectView object) noexcept {
        return object.store32(0x014, 8);
    }
    static bool RequestResume(ObjectView object) noexcept {
        return object.store32(0x014, 1);
    }
};
struct CSTEP {
    static bool constructor(ObjectView object) noexcept {
        return object.store32(0x000, 0);
    }
};
struct CSTEP_BATCH {
    static bool Uninit(ObjectView object) noexcept {
        return object.store32(0x020, 0);
    }
};
struct xpApiEnv {
    // The original uses symbol initCARD(long). The 12-byte body does not
    // visibly depend on the long argument, but this does NOT prove that the
    // calling context ignores it.
    static bool initCARD(ObjectView object, std::int32_t /*unknown_argument*/) noexcept {
        return object.store32(0x304, 1);
    }
};
}  // namespace fft_b01

extern "C" int fft_b01_named_cpp_method(
    std::uint32_t elf_entry, std::uint8_t* object, std::size_t object_size,
    std::uint32_t argument_r1) noexcept {
    const fft_b01::ObjectView view{object, object_size};
    bool successful=false;
    switch (elf_entry) {
    case 0x000b3518u: successful=fft_b01::CINPUT_DATA::constructor(view); break;
    case 0x000b9f7cu: successful=fft_b01::CTHREAD::RequestExit(view); break;
    case 0x000b9facu: successful=fft_b01::CTHREAD::RequestSuspend(view); break;
    case 0x000b9fb8u: successful=fft_b01::CTHREAD::RequestResume(view); break;
    case 0x000bdb60u: successful=fft_b01::CSTEP::constructor(view); break;
    case 0x000be1dcu: successful=fft_b01::CSTEP_BATCH::Uninit(view); break;
    case 0x0028de9cu: successful=fft_b01::xpApiEnv::initCARD(
        view, static_cast<std::int32_t>(argument_r1)); break;
    default: return -2;
    }
    return successful ? 0 : -1;
}

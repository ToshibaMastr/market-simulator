#include <math.h>
#include <stdint.h>
#include <sys/types.h>


int crosspoint(const float* asks, const float* bids, uint32_t omax, float *volume) {
    float sm = 0.0, vm = 0.0;

    for (uint32_t k = 0; k < omax; sm += bids[k++]);

    uint32_t j;
    for (j = 0; sm > vm; j++) {
        vm += asks[j]; sm -= bids[j];
    }

    *volume = fminf(vm, sm);

    return j - 1;
}

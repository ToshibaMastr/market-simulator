#include <math.h>
#include <sys/types.h>

int crosspoint(const float* asks, const float* bids, uint omax, float *volume) {
    float sm = 0.0, vm = 0.0;

    for (uint k = 0; k < omax; sm += bids[k++]);

    uint j;
    for (j = 0; sm > vm; j++) {
        vm += asks[j]; sm -= bids[j];
    }

    *volume = fminf(vm, sm);


    return j - 1;
}


int old_crosspoint(const float* asks, const float* bids, uint omax, float *volume) {
    uint bi = omax - 1;
    uint si = 0;

    float volume_bids = bids[bi], volume_asks = asks[si];

    while (bi > si) {
        if (volume_bids < volume_asks) {
            volume_bids += bids[bi];
            bi -= 1;
        } else {
            volume_asks += asks[si];
            si += 1;
        }
    }

    *volume = fminf(volume_bids, volume_asks);

    return bi;
}

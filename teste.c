void decode1(long *xp, long *yp, long *zp) {
    long temp_x = *xp;
    long temp_y = *yp;
    long temp_z = *zp;

    *yp = temp_x;
    *zp = temp_y;
    *xp = temp_z;
}


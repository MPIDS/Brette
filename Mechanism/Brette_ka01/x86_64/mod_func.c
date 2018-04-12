#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _hhmfb_reg(void);
extern void _NaBrette_point_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," hhmfb.mod");
    fprintf(stderr," NaBrette_point.mod");
    fprintf(stderr, "\n");
  }
  _hhmfb_reg();
  _NaBrette_point_reg();
}

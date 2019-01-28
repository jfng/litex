import os

from migen import *

from litex.soc.interconnect import wishbone


class Minerva(Module):
    name = "minerva"
    endianness = "little"
    gcc_triple = ("riscv64-unknown-elf", "riscv32-unknown-elf")
    gcc_flags = "-D__minerva__ -march=rv32i -mabi=ilp32"
    linker_output_format = "elf32-littleriscv"

    def __init__(self, platform, cpu_reset_address, variant=None):
        assert cpu_reset_address is 0, "The reset address is currently hardcoded to 0."
        assert variant is None, "Unsupported variant %s" % variant

        self.reset = Signal()
        self.ibus = wishbone.Interface()
        self.dbus = wishbone.Interface()
        self.interrupt = Signal(32)

        ###

        self.cpu_ports = {
            "i_clk": ClockSignal(),
            "i_rst": self.reset | ResetSignal(),

            "i_external_interrupt": self.interrupt,
            "i_timer_interrupt": 0,

            "o_ibus_adr": self.ibus.adr,
            "o_\\ibus_dat_w$7 ": self.ibus.dat_w,
            "o_\\ibus_sel$8 ": self.ibus.sel,
            "o_ibus_cyc": self.ibus.cyc,
            "o_ibus_stb": self.ibus.stb,
            "o_\\ibus_we$9 ": self.ibus.we,
            "o_ibus_cti": self.ibus.cti,
            "o_ibus_bte": self.ibus.bte,
            "i_ibus_dat_r": self.ibus.dat_r,
            "i_ibus_ack": self.ibus.ack,
            "i_ibus_err": self.ibus.err,

            "o_dbus_adr": self.dbus.adr,
            "o_dbus_dat_w": self.dbus.dat_w,
            "o_dbus_sel": self.dbus.sel,
            "o_dbus_cyc": self.dbus.cyc,
            "o_dbus_stb": self.dbus.stb,
            "o_dbus_we": self.dbus.we,
            "o_dbus_cti": self.dbus.cti,
            "o_dbus_bte": self.dbus.bte,
            "i_dbus_dat_r": self.dbus.dat_r,
            "i_dbus_ack": self.dbus.ack,
            "i_dbus_err": self.dbus.err
        }

        vdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "verilog")
        platform.add_sources(os.path.join(vdir), "minerva.v")

    def do_finalize(self):
        self.specials += Instance("minerva_cpu", **self.cpu_ports)

// ----------------------------------------------------------------------------
// AUTHOR'S EMAIL : kobzar
// ----------------------------------------------------------------------------
// DESCRIPTION    :
// ----------------------------------------------------------------------------

`ifndef INC_HSR_ETH_DR_SEQ
`define INC_HSR_ETH_DR_SEQ


class hsr_eth_dm_seq extends sr_eth_base_seq;

  sr_eth_dm dm;
  sr_eth_fm fm;

  `uvm_object_utils(hsr_eth_dm_seq)
  function new (string name = "hsr_eth_dm_seq");
    super.new(name);
    dm = new("dm");
  endfunction
  task pre_body(
    input bit bla, hey,
    output bit gkgkgk
  );
    uvm_mem mem;
    super.pre_body();
    if(dm == null) `uvm_fatal(get_full_name(), $sformatf("dm should be set in %0s", get_full_name()))
    if(fm == null) `uvm_fatal(get_full_name(), $sformatf("fm should be set in %0s", get_full_name()))

  endtask
endclass
`endif // !INC_HSR_ETH_DR_SEQ
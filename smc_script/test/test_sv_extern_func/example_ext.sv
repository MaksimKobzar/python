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

  extern function new(
    string name = "hsr_eth_dm_seq"
  );
  extern task pre_body ();

  extern virtual function bit [`AA-1:0] body (
    input bit a = 0
  );
endclass


function hsr_eth_dm_seq::new(string name = "hsr_eth_dm_seq");
  super.new(name);
  dm = new("dm");
endfunction

task hsr_eth_dm_seq::pre_body();
  uvm_mem mem;
  super.pre_body();
  if(dm == null) `uvm_fatal(get_full_name(), $sformatf("dm should be set in %0s", get_full_name()))
  if(fm == null) `uvm_fatal(get_full_name(), $sformatf("fm should be set in %0s", get_full_name()))
endtask

virtual function bit [`AA-1:0] hsr_eth_dm_seq::body(
  input bit a = 0
);
  `uvm_info(get_full_name(), "is started", UVM_MEDIUM)

  forever begin
    fm.get_next_item(frame);
    dm.add_dm_item(frame);
    fm.item_done();
    fm.put_response(frame);
  end

  `uvm_info(get_full_name(), "is ended", UVM_MEDIUM)
endtask

`endif

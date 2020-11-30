// ----------------------------------------------------------------------------
// AUTHOR'S EMAIL : kobzar
// ----------------------------------------------------------------------------
// DESCRIPTION    :
// ----------------------------------------------------------------------------

/*

aaa*/

// cqwq
// ----------

/*

swwqs

*/


`ifndef INC_SR_ETH_DR_SEQ/*
dwqwq

*/

`define INC_SR_ETH_DR_SEQ//LK::L:LKK:L

/*
dwqwq

*/

/*

*/

class sr_eth_dm_seq extends sr_eth_base_seq;

  sr_eth_dm dm;
  sr_eth_fm fm;

  `uvm_object_utils(sr_eth_dm_seq)

  function new(string name ="sr_eth_dm_seq");
    super.new(name);
  endfunction

  task pre_body();
    uvm_mem mem;
    super.pre_body();
    if(dm == null) `uvm_fatal(get_full_name(), $sformatf("dm should be set in %0s", get_full_name()))
    if(fm == null) `uvm_fatal(get_full_name(), $sformatf("fm should be set in %0s", get_full_name()))
  endtask

  task body();
    `uvm_info(get_full_name(), "is started", UVM_MEDIUM)

    forever begin
      fm.get_next_item(frame);
      dm.add_dm_item(frame);
      fm.item_done();
      fm.put_response(frame);
    end

    `uvm_info(get_full_name(), "is ended", UVM_MEDIUM)
  endtask

endclass


`endif /*
faweqf

qwd
wq
wq

aaa//*/ 



class smc_llc_env_cfg extends uvm_object;

  virtual smc_llc_env_if vif;

  bit has_cov = 1;
  bit has_check = 1;

  csr_block_llc reg_model;
  !<CDVE_HAS_AGENT_CFG_INST!>
  !<CDVE_AGENT_CFG_INST!>

  `uvm_object_utils_begin(smc_llc_env_cfg)
    `uvm_field_int(has_cov,   UVM_DEFAULT)
    `uvm_field_int(has_check, UVM_DEFAULT)
    !<CDVE_AGENT_CFG_UTILS!>
  `uvm_object_utils_end

  function new(string name = "smc_llc_env_cfg");
    super.new(name);
  endfunction

  virtual function void build();
    ['if(reg_model == null) begin', '  reg_model = csr_block_llc::type_id::create({get_full_name(), ".reg_model"});', '  reg_model.build();', '  reg_model.lock_model();', '  reg_model.reset();', '  if(has_cov) reg_model.set_coverage(UVM_CVR_ADDR_MAP + UVM_CVR_FIELD_VALS);', 'end']
    !<CDVE_AGENT_CFG_CREATE!>
    `uvm_info("ENV_CFG", $sformatf("After build print:\n%0s", this.sprint()), UVM_LOW)
  endfunction

endclass

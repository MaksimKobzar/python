
module module_example
#(
  parameter CNT_WIDTH = 4
)
(
  input clk,    // Clock
  input wire rst_n,  // Asynchronous reset active low
  input logic clk_en, // Clock Enable
  output logic [1:0] flag
);

  logic [CNT_WIDTH-1:0] cnt;

  always @(posedge clk, negedge rst_n) begin
    if(~rst_n) begin
      cnt <= {CNT_WIDTH{1'b0}};
    end else if(clk_en) begin
      cnt <= cnt + 1;
    end
  end

  assign flag[0] = (cnt == 4'h1001);
  assign flag[1] = (cnt == 4'h0110);

endmodule
{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem ( system:
    let
      pkgs = import nixpkgs { inherit system; };
    in {
      devShell = pkgs.mkShell {
        name = "django application";
        buildInputs = with pkgs; [
          (pkgs.python3.withPackages (python-pkgs:
            with python-pkgs; [
              django
              mysqlclient
              apscheduler
              pip
            ]
          ))
          # mysql80
        ];
      };
    });
}

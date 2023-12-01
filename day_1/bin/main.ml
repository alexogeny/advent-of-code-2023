(** each line contained a value that needs recovery*)
(** on each line, you combine the first digit and last digit (in order) to form a single 2 digit number*)
(** each calibration value is a line item. we need to find the sum of all of them.*)

let read_file_to_list filename =
  let input_channel = open_in filename in
  let rec read_lines acc =
    match input_line input_channel with
    | line -> read_lines (line :: acc)
    | exception End_of_file -> List.rev acc
  in
  let lines = read_lines [] in
  close_in input_channel;
  lines

let remove_empty_last_line lines =
  match List.rev lines with
  | "" :: t -> List.rev t
  | _ -> lines

let read_lines filename =
  filename
  |> read_file_to_list
  |> remove_empty_last_line
  |> Array.of_list

let () =
  let lines = read_lines "input.txt" in
  Array.iter (fun line -> print_endline line) lines

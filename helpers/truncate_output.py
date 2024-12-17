##----USER SET OPTIONS----------------------------------------------##
truncation_trace_text = "...truncated..."
limit_number_lines = 20 # SET THE LIMIT OF LINES IN THE OUTPUT; EVERYTHING AFTER WILL BE TRUNCATED TO `...truncated...` or what `truncation_trace_text` set to
limit_to_working_directory = False # Set to `False` if want recursive and to process all notebooks in sub-directories below location of this script
edited_notebook_name_prefix = "TRUNCATED_" 
##----END OF USER SET OPTIONS SECTION-------------------------------##
import os
import fnmatch
import nbformat as nbf
pattern_to_match = "*.ipynb"


def truncate_long_notebook_output(filepath):
    '''
    Use nbformat to process all Jupyter `.ipynb` files to limt size of output
    to setting for `limit_number_lines`

    The removed part will be indicated with `truncation_trace_text`

    In relation to SO Post https://stackoverflow.com/q/79136448/8508004
    '''
    ntbk = nbf.read(filepath, nbf.NO_CONVERT)
    dirpath, notebook_name = os.path.split(filepath)
    cells_for_new_version = []
    limit_exceeded_for_notebook = False
    '''
    size_estimate_dict = {}
    for cell in ntbk.cells:
        if cell.cell_type == 'code':
            size_estimate_dict[cell.execution_count] = len(str(cell.outputs))
    out_size_info = [k for k, v in sorted(size_estimate_dict.items(), key=lambda item: item[1],reverse=True)]
    out_size_info
    '''
    try:
        for cell in ntbk.cells:
            if cell.cell_type == "code":
                # MAIN PURPOSE: Take output in code cell and split on newlines & then 
                # truncate to setting for `limit_number_lines`, appending 
                # `truncation_trace_text`
                current_outputs = []
                
                num_lines = 0
                lines_in_current_output=0
                for idx,the_output_item in enumerate(cell.outputs):
                    if 'text' in the_output_item:
                        num_lines += len(str(the_output_item['text']).split('\n'))
                        # see if exceeds limit yet
                        if num_lines > limit_number_lines:
                            #print("\n".join(the_output_item['text'].split()[:limit_number_lines-lines_in_current_output]))
                            text_for_output = "\n".join(the_output_item['text'].split('\n')[:limit_number_lines-lines_in_current_output]) + '\n' + truncation_trace_text
                            the_output_item['text'] = text_for_output
                            current_outputs.append(the_output_item)
                            limit_exceeded_for_notebook = True
                            break
                        else:
                            current_outputs.append(the_output_item)
                            lines_in_current_output += num_lines
                    elif 'data' in the_output_item:
                        # JUST A STUB FOR NOW!!!!!!
                        # Note that this code isn't quite fleshed out for other output yet. 
                        # In particular, if you have dataframes it counts lines and just skips the next one in that output with no indicator about truncation. 
                        # It doesn't truncate any dataframe itself in the middle, say if you have the options set to print all the rows.
                        # what it will do for now is stop adding things if this
                        # results in exceeding limit after first hit
                        # current_outputs.append(the_output_item)
                        # num_lines += len(str(the_output_item['data']).split('\n'))
                        num_lines += len(str(the_output_item['data']).split(','))
                        # see if exceeds limit yet
                        if num_lines > limit_number_lines:
                            limit_exceeded_for_notebook = True
                            break
                        else:
                            current_outputs.append(the_output_item)
                    else:
                        current_outputs.append(the_output_item)
                        num_lines += len(str(the_output_item).split('\n'))
                        # see if exceeds limit yet
                        if num_lines > limit_number_lines:
                            limit_exceeded_for_notebook = True
                            break
                cell.outputs = current_outputs
                cells_for_new_version.append(cell)
            else:
                cells_for_new_version.append(cell)
        if limit_exceeded_for_notebook:
            new_ntbk_fp = os.path.join(dirpath, edited_notebook_name_prefix + notebook_name)
            print(f"Output in {filepath} above threshold seen and so a NEW version has been made: `{new_ntbk_fp}`.")
            new_ntbk = ntbk
            new_ntbk.cells = cells_for_new_version
            nbf.write(new_ntbk, new_ntbk_fp, version=nbf.NO_CONVERT)
            truncated = True
        else:
            print(f"Output in {filepath} not above threshold and so no new version made.")
            truncated = False
    except UnboundLocalError: # This will allow it to work if you put this code in a **FRESH** new notebook and run without saving first so that there is no cell to be read
        pass
    
    return truncated




# apply to all notebooks in the current working directory 
def apply_truncate_output_to_all_notebooks():
    if limit_to_working_directory:
        for filename in os.listdir('.'):
            if filename.upper().endswith((pattern_to_match.upper()[1:])): # based on https://stackoverflow.com/a/5351968/8508004
                # if it is a notebook then run the main function
                truncate_long_notebook_output(filename)
    # `os.walk()` starting in the current working directory as 'root' based on 
    # https://stackoverflow.com/a/54673093/8508004
    else:
        for root, dirs, files in os.walk('.'):
            for filename in files:
                #if fnmatch.fnmatch(filename, pattern_to_match): # based on https://stackoverflow.com/a/76996927/8508004
                if filename.upper().endswith((pattern_to_match.upper()[1:])) and '.local/share/Trash/' not in (os.path.join(root, filename)): # based on https://stackoverflow.com/a/5351968/8508004, plus don't want stuff in trash while working on with MyBInder session
                    # if it is a notebook then run the main function
                    truncate_long_notebook_output(os.path.join(root, filename))
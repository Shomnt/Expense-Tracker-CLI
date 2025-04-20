<h1>Expense Tracker CLI</h1>
<h2>Commands</h2>
<p><b>add</b>: add new expenses</p>
<p><b>update</b>: update expenses</p>
<p><b>delete</b>: delete expenses</p>
<p><b>list</b>: display a list of expenses</p>
<p><b>summary</b>: display summary reports of expenses</p>

<h2>Examples</h2>
<code>python main.py -h</code>
<p><b>Output</b>: @help informations...</p>
<code>python main.py add --description "Lunch" --amount 20</code>
<p><b>Output</b>: # Expense added successfully (ID: 0)</p>
<code>python main.py add --description "Dinner" --amount 10</code>
<p><b>Output</b>: # Expense added successfully (ID: 1)</p>
<code>python main.py list </code>
<p><b>Output</b>: @list of expenses...</p>
<code>python main.py summary</code>
<p><b>Output</b>: # Total expenses: $30</p>
<code>python main.py summary --month 8</code>
<p><b>Output</b>: # Total expenses for August: $20</p>
<code>python main.py delete --id 1</code>
<p><b>Output</b>: # Expense deleted successfully</p>

<p><strong>Read more in help text.</strong></p>

<a href=https://roadmap.sh/projects/expense-tracker>URL</a>

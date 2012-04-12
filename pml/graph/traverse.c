/*
 * File: Traverse.c
 * Traverse graph built by parser, printing nodes visited.
 * $Id: traverse.c,v 1.2 2008/07/25 22:06:53 jnoll Exp $
 * Author: John Noll & Jigar Shah 
 * Javascript calls inserted by Don Browne
 * Date Written: Aug 10 2003
 * Date Last Modified: 08-APR-2012
 *
 */

# include <stdio.h>
# include <errno.h>
# include <stdlib.h>
# include <string.h>
# include <libgen.h>		/* basename */
# include <unistd.h>
# include <pml/scanner.h>
# include <pml/parser.h>
# include <pml/tokens.h>

typedef enum { FLOW = 0x1, XML=0x2, ANON=0x4, NO_RESOURCE=0x8, 
	       NO_LINK_LABELS=0x10, JS_ANNOTATIONS=0x20} output_t;
output_t graph_type = 0;

typedef enum { GRAY, BLACK, WHITE } node_color_t;

int node_num = 0;
int node_count = 0;
char *col_brk[250];
Node col_heads[250];
int cols=0, num_heads=0;



/* Provide main with a prototype to eliminate compiler warnings. */
extern int main (
# ifdef ANSI_PROTOTYPES
    int		/* argc */,
    String []	/* argv */
# endif
);

char *node_type(int type) 
{
    switch (type) {
    case (ACTION): return "action"; break;
    case (BRANCH): return "branch"; break;
    case (ITERATION): return "iter"; break;
    case (SELECTION): return "select"; break;
    case (SEQUENCE): return "sequence"; break;
    case (PROCESS): return "process"; break;
    case (JOIN): return "join"; break;
    case (RENDEZVOUS): return "rend"; break;
    default: return "unknown"; break;

    }
}


char *node_shape(int type) 
{
    switch (type) {
    case (ACTION): 
	if (graph_type & NO_RESOURCE) {
	    return "box, style=rounded"; 
	} else {
	    return "Mrecord"; 
	}
	break;
    case (ITERATION): return "diamond"; break; /* XXX Never happens. */
    case (SELECTION): return "circle, fixedsize = true"; break;
    case (JOIN): return "circle, fixedsize = true"; break;
    case (BRANCH): return "circle, fixedsize = true, style=filled"; break;
    case (RENDEZVOUS): return "circle, fixedsize = true, style=filled"; break;
    case (PROCESS): return "diamond"; break;

    default: fprintf(stderr, "Help! %s is unknown!\n", node_type(type)); return "plaintext"; break;

    }
}

char *op_to_string(int op)
{
    switch(op) {
    case (OR): return "||"; break;
    case (AND): return "&&"; break;
    case (EQ): return "=="; break;
    case (NE): return "!="; break;
    case (LE): return "<="; break;
    case (GE): return ">="; break;
    case (LT): return "<"; break;
    case (GT): return ">"; break;
    case (NOT): return "!"; break;
    case (DOT): return "."; break;
    case (QUALIFIER): return "(qual)"; break;
    case (ID): return "ID"; break;
    }
    return "I don't know";
}

void insert_iteration_links(Node from, Node to)
{
    Node p;
    int i;

    fprintf(stderr, "LOOP: %s (%ld) -> %s (%ld)\n", from->name, (long)from,
	   to->name, (long) to);

    /* Look for an unseen node to skip to. */
    for (i = 0; (p = (Node) ListIndex(from->successors, i)); i++) {
	if ((node_color_t)p->data == WHITE) {
	    printf("%s_%ld -> %s_%ld [label=\"skip\", weight=0]\n",
		   to->name, (long)to, p->name, (long)p);
	}
    }

}

void print_resources(Tree t)
{
    
    if (t) {
	if (IS_ID_TREE(t)) {
	    if (TREE_ID(t)[0] == '"') {
		int i;
		for (i = 1; i < strlen(TREE_ID(t)); i++) {
		    if (TREE_ID(t)[i] == '"') break;
		    putchar(TREE_ID(t)[i]);
		}
		printf(" ");
	    } else {
		printf("%s", TREE_ID(t));
	    }
	} else {
	    print_resources(t->left);
		printf(",\\n");
	    print_resources(t->right);
	}
    } else {
	printf("(none)");
    }
}

void print_link(Node from, Node to, int weight)
{
    static int col = 0;
    int i, new_col = 0;
    for (i = 0; i < cols; i++) {
	if(strcmp(col_brk[i], from->name) == 0) {
	    col++;
	    new_col = 1;
	    col_heads[num_heads++] = to;
	    break;
	}
    }

    if (weight != 0) {
	if (new_col) {
	    /* Emit column separator node. */
	    printf("start_%d [shape = point, label = \"\"];\n",
		   col);
	    printf("{ rank = same; %s_%ld; start_%d; }\n", 
		   from->name, (long)from, col);
#ifdef OLD
	    /* Connect from to separator.  */
	    printf("%s_%ld -> start_%d [weight=%d, style=%s];\n",
		   from->name, (long)from, col,  weight, weight == 0 ? "invis" : "solid");
#endif
	    printf("%s_%ld -> start_%d [weight=%d, style=%s, arrowhead = none,",
		   from->name, (long)from, col, weight, weight == 0 ? "invis" : "solid"); 

	} else {
	    printf("%s_%ld -> %s_%ld [weight=%d, style=%s",
		   from->name, (long)from, to->name, (long)to, weight, weight == 0 ? "invis" : "solid");
	}

	if (!(graph_type & (ANON|NO_LINK_LABELS))) {
	    if (from->type == ACTION) {
		printf(", labelfloat=\"true\", fontname=TimesItalic, labelfontcolor=\"black\", taillabel=\"");
		print_resources((from->provides));
		printf("\"");
	    }
	}
	if (new_col) {

	    printf("];\n") ;	/* Finish link in progress*/

	    /* Emit column start node, then arrow from labeled diamond. */
	    printf("end_%d [shape = point, label = \"\"];\n",
		   col);

	    printf("{ rank = same; end_%d; %s_%ld; }\n", 
		   col, to->name, (long)to);
	    printf("end_%d -> %s_%ld [weight=%d, style=%s]",
		   col, to->name, (long)to, weight, weight == 0 ? "invis" : "solid");

	    printf("end_%d -> start_%d [weight=%d, style=%s,  arrowhead = none,",
		   col, col, weight, weight == 0 ? "invis" : "solid");
	    node_count = 0;
	}
	if (!(graph_type & (ANON|NO_LINK_LABELS))) {
	    if (to->type == ACTION) {
		printf(", labelfloat=\"true\", fontname=TimesItalic, fontcolor=\"BLACK\", headlabel=\"");
		print_resources((to->requires));
		printf("\"") ;
	    }
	}
	printf("] ;\n") ;	/* Finish link in progress*/
    } else {
/*	printf("%ld -> %ld [label=\"again\", weight=%d, style=%s, headport=\"ne\", tailport=\"se\"] ;\n", */
	printf("%s_%ld -> %s_%ld [weight=%d] ;\n",
	       from->name, (long)from, to->name, (long)to, weight);
    }
}

void name_node(Node n)
{
    char buf[512];

    if (strcmp(n->name, "(anonymous)") == 0) {
	/*free(n->name);*/
	sprintf(buf, "%s_%d", node_type(n->type), node_num++);
	n->name = strdup(buf);
    }

    if (n->type == PROCESS) {
	/*free(n->name);*/
	n->name = strdup("start");
    }
    /* This hack detects sink. */
    if (n->next == NULL) {
	/*free(n->name);*/
	n->name = strdup("end");
    }
    if (graph_type != XML) {
	printf("%s_%ld [shape=%s, ", n->name, (long)n, node_shape(n->type));
	if (n->type == PROCESS) {
    printf("label=\"%s\"",n->name);
    if (graph_type & JS_ANNOTATIONS) 
    {
        printf(", href=\"javascript:alert('Name: %s\\n", n->name, n->name);
        if (n->tool != NULL) 
        {
            printf("Tool:%s\\n",n->tool);
        }
        if (n->agent) 
        {
            printf("Agent: ");
            print_resources(n->agent);
            printf("\\n");
        }
        if (n->requires) 
        {
            printf("Requires: ");
            print_resources(n->requires);
            printf("\\n");
        }
        if (n->provides) 
        {
            printf("Provides: ");
            print_resources(n->provides);
            printf("\\n");
        }
        printf("')\"");
    }
    printf("];\n");
	} else 	if (!(graph_type & (ANON)) && (n->type == ACTION)) {
	    if (!(graph_type & NO_RESOURCE)) {
		printf("label=");
		printf("\"{");
		print_resources(n->requires);
		printf("|%s|", n->name);
		print_resources(n->provides);
		printf("}\"];\n");
	    } 
        else 
        {
   printf("label=\"%s\"",n->name);
        if (graph_type & JS_ANNOTATIONS) 
        {
            printf(", href=\"javascript:alert('Name: %s\\n", n->name, n->name);
            if (n->tool != NULL) 
            {
                printf("Tool:%s\\n",n->tool);
            }
            if (n->agent) 
            {
                printf("Agent: ");
                print_resources(n->agent);
                printf("\\n");
            }
            if (n->requires) 
            {
                printf("Requires: ");
                print_resources(n->requires);
                printf("\\n");
            }
            if (n->provides) 
            {
                printf("Provides: ");
                print_resources(n->provides);
                printf("\\n");
            }
            printf("')\"");
        }
        printf("];\n");
   
	    }
	} else {
	    printf("label=\"\"];\n");
	}
    }
}

void has_cycle(Node n, int name)
{
    int i;
    Node child;

    n->data = (void *)GRAY;
    node_count++;

    if (graph_type == XML) {
	printf("<%s name=\"%s\">\n", node_type(n->type), n->name);
    }
    if (name) {
	if (n->type == SELECTION || n->type == BRANCH) {
	    printf("{ rank = same;\n");
	}
	if (n->type == SEQUENCE) {
	    printf("{ subgraph cluster_%s_%ld;\n", n->name, (long)n);
	    printf("  style = filled; color = lightgrey; label = %s\n", 
		   n->name);
	}
	for (i = 0; (child = (Node) ListIndex(n->successors, i)); i++) {
	    name_node(child);
	}
	if (n->type == SELECTION || n->type == BRANCH || n->type == SEQUENCE) {
	    printf("}\n");
	}
    }

    for (i = 0; (child = (Node) ListIndex(n->successors, i)); i++) {
	if (graph_type != XML) {
	    if (!name) {
		print_link(n, child, 
			   (node_color_t) child->data == GRAY ? 0 : 1);
	    }
	}
	if ((node_color_t)child->data == WHITE) {
	    has_cycle(child, name);
	}
    }

    if (graph_type == XML) {
	printf("</%s>\n", node_type(n->type));
    }
    n->data = (void *)BLACK;
}



void traverse(Node n, int name)
{
    Node p = n;
    /* Mark all nodes WHITE to begin. */
    while (p) {
	p->data = (void *) WHITE;
	p = p->next;
    }

    /* Look for cycles. */
    has_cycle(n, name);
}



void name_nodes(Node n)
{
    int i; 
    Node child;

    /* Column head nodes should be same rank as first node after 'start' */
    for (i = 0; (child = (Node) ListIndex(n->successors, i)); i++) {    
	col_heads[num_heads++] = child;
    }
    name_node(n);
    traverse(n, 1);
}

static String usage = "\
usage: %s [options] [file ...]\n\
    -a  don't print any labels (anonymous)\n\
    -c  new column after this node\n\
    -f  include control flow edges (default)\n\
    -j  include Javascript annotations for web graphing\n\
    -R  don't print resource names\n\
    -L  don't label edges with resources\n\
    -x  emit XML (not working)\n\
";


int main(argc, argv)
    int    argc;
    String argv [ ];
{
    int i, c, status;

    filename = "-";
    status = EXIT_SUCCESS;

    while ((c = getopt (argc, argv, "ac:dfjLmxhR?")) != EOF) {
	switch (c) {
	case 'a':
	    graph_type |= ANON;
	    break;

	case 'c':
	    col_brk[cols++] = optarg;
	    break;

	case 'f':
	    graph_type |= FLOW;
	    break;

    case 'j':
	    graph_type |= JS_ANNOTATIONS;
	    break;

	case 'R':
	    graph_type |= NO_RESOURCE;
	    break;

	case 'L':
	    graph_type |= NO_LINK_LABELS;
	    break;

	case 'x':
	    graph_type = XML;
	    break;

	case 'h':
	    printf (usage, argv[0]);
	    exit(EXIT_SUCCESS);
	    break;

	case '?':
	    exit(EXIT_FAILURE);
	    break;
	}
    }

    if (graph_type == 0) {
	graph_type = (FLOW);
    }
    do {
	if (optind < argc) {
	    filename = argv [optind];
	    lineno = 1;
	}

	if (strcmp (filename, "-") == 0) {
	    filename = "stdin";
	    yyin = stdin;

	    if (yyparse ( ))
		status = EXIT_FAILURE;

	} else if ((yyin = fopen (filename, "r")) != NULL) {
	    if (yyparse ( ))
		status = EXIT_FAILURE;

	    fclose (yyin);

	} else {
	    fprintf (stderr, "%s: ", argv [0]);
	    perror (filename);
	    status = EXIT_FAILURE;
	}

    } while (++ optind < argc);

    if (status != EXIT_FAILURE) {
	if (program) {
	    char *p, *name = basename(filename);
	    name = strtok(name, ".");
	    for (p = name; *p; p++) {
		if (*p == '-') *p = '_';
	    }
	    if (graph_type != XML) {
		printf("digraph %s {\n", name);
		printf("  rankdir = TB;\n");
		printf("  ordering = out;\n");
/*
		printf("process [shape=plaintext, label=\"%s\"];\n", filename);
*/

	    }
	    name_nodes(program->source);
	    node_count = 0;
	    traverse(program->source, 0);
	    printf("{ rank = same;\n");
	    for (i = 0; i < num_heads; i++) {
		printf("  %s_%ld; \n", col_heads[i]->name, (long)col_heads[i]);
	    }
	    printf(" }\n");
	    if (graph_type != XML) {
		printf("}\n");
	    }
	}
    }
    exit (status);
}

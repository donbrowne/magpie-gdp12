/*
 * File: pmlpic.c
 * Traverse graph built by parser, printing nodes visited as pic boxes.
 * $Id: traverse.c,v 1.1 2005/05/27 01:58:57 jnoll Exp $
 * Author: John Noll & Jigar Shah
 * Date Written: Aug 10 2003
 * Date Last Modified: Aug 11 2003
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

#define LABEL_LINKS 1

typedef enum { FLOW = 0x1, XML=0x2, ANON=0x4} output_t;
output_t graph_type = 0;

typedef enum { GRAY, BLACK, WHITE } node_color_t;

int node_num = 0;

static String usage = "\
usage: %s [options] [file ...]\n\
    -d  include dominator edges\n\
    -f  include control flow edges (default)\n\
    -m  include matching edges\n";


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
    case (ACTION): return "box, style=rounded"; break;
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
	    printf("%ld -> %ld [label=\"skip\", weight=0]\n", (long)to, (long)p);
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
	    } else {
		printf("\"%s\" ", TREE_ID(t));
	    }
	} else {
	    print_resources(t->left);
	    print_resources(t->right);
	}
    } else {
	printf("\"(none)\" ");
    }
}

void print_link(Node from, Node to, int weight)
{
    printf("arrow right; box rad 0.1 \"%s\";\n", to->name);
}

void name_node(Node n)
{
    char buf[512];
    fprintf(stderr, "%s_%d\n", node_type(n->type), node_num++);
    if (strcmp(n->name, "(anonymous)") == 0) {
	free(n->name);
	sprintf(buf, "%s_%d", node_type(n->type), node_num++);
	n->name = strdup(buf);
    }

    if (n->type == PROCESS) {
	free(n->name);
	n->name = strdup("start");
    }
    /* This hack detects sink. */
    if (n->next == NULL) {
	free(n->name);
	n->name = strdup("end");
    }
}

void has_cycle(Node n, int name)
{
    int i;
    Node child;

    n->data = (void *)GRAY;
    if (name) {
	if (n->type == SEQUENCE) {
	    printf("\n");
	}
	for (i = 0; (child = (Node) ListIndex(n->successors, i)); i++) {
	    name_node(child);
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
    name_node(n);
    traverse(n, 1);
}



int main(argc, argv)
    int    argc;
    String argv [ ];
{
    int c, status;

    filename = "-";
    status = EXIT_SUCCESS;

    while ((c = getopt (argc, argv, "adfmxh?")) != EOF) {
	switch (c) {
	case 'a':
	    graph_type |= ANON;
	    break;

	case 'f':
	    graph_type |= FLOW;
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
	graph_type = FLOW;
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
	    printf("\n.PS\n");
	    name_nodes(program->source);
	    traverse(program->source, 0);
	    printf("\n.PE\n");
	}
    }
    exit (status);
}

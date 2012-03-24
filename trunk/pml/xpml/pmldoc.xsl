<!-- $Id: pmldoc.xsl,v 1.4 2005/11/28 21:47:13 jnoll Exp $ -->
<!-- Convert XPML to HTML ``process document'' format. -->
<!DOCTYPE project [
  <!ENTITY institution     SYSTEM "institution.xml">
]>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:exsl="http://exslt.org/common"
                extension-element-prefixes="exsl">
<xsl:import href="html.xsl"/>
<xsl:import href="style.xsl"/>

<xsl:strip-space elements="*"/>
<xsl:output method="html" indent="yes" />

<xsl:template match="/">
 <xsl:apply-templates/>
</xsl:template>

<xsl:template match="document">
<html>
  <head>
    <title><xsl:value-of select="head/title"/>
    </title>
  </head>

  <body  bgcolor="#ffffff">
   <xsl:apply-templates/>
  </body>
</html>
</xsl:template>

<xsl:template match="head">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="title">
  <h1><xsl:value-of select="text()"/></h1>
</xsl:template>

<xsl:template match="subtitle">
  <h2><xsl:value-of select="text()"/></h2>
</xsl:template>

<xsl:template match="author">
  <h2><xsl:value-of select="text()"/></h2>
</xsl:template>

<xsl:template match="institution">
  <h3><xsl:value-of select="text()"/></h3>
</xsl:template>
<xsl:template match="abstract">
<hr/>
  <i><xsl:value-of select="text()"/></i>
<hr/>
</xsl:template>

<xsl:template match="body">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="section">
<h2>
<xsl:number level="multiple" 
	    count="section|process|sequence|iteration|branch|selection" 
	    format="1.1. "/>
<xsl:value-of select="translate(@name, '_', ' ')"/>
</h2>
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="process">
<form method="POST" action="update.cgi">
<xsl:if test="@pid">
  <input type="hidden" name="PID" value="{@pid}"/>
</xsl:if>
<xsl:variable name="actions">
  <xsl:for-each select=".//action">
    <xsl:value-of select="@name"/>
    <xsl:text> </xsl:text>
  </xsl:for-each>
</xsl:variable>
<input type="hidden" name="actions" value="{$actions}"/>
<h2>
<xsl:number level="multiple" 
	    count="section|process|sequence|iteration|branch|selection|action|req" 
	    format="1.1. "/>
Tasks
</h2>
Perform the following tasks as specified.
<xsl:if test="@pid">
<p>Check the box next to an action's name when finished; click `update' to notify PEOS of finished actions and update action state.</p>
</xsl:if>
<ol>
  <xsl:apply-templates/>
</ol>
</form>
</xsl:template>

<xsl:template match="submit">
  <input type="submit" name="op" value="update"/>
  <input type="reset" value="reset"/>
</xsl:template>

<xsl:template match="action">
<h3>
<li>
<xsl:value-of select="translate(@name, '_', ' ')"/>
<xsl:if test="@state">
  <xsl:choose>
    <xsl:when test="@state='FINISHED' or @state='PENDING'">
      <input type="checkbox" name="{@name}" value="finish" checked="checked"/>
    </xsl:when>
    <xsl:otherwise>
      <input type="checkbox" name="{@name}" value="finish"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:if>
</li>
</h3> 
    <div class="scroll">
    <table style="width: 100%;" border="0" cellpadding="2" cellspacing="0">
     <tbody>
      <tr>
      <xsl:call-template name="detail-pane"/>
      </tr>
     </tbody>
    </table>
    </div>

</xsl:template>

<xsl:template match="iteration">
<h3>
<li>
  <xsl:value-of select="translate(@name, '_', ' ')"/>
</li>
</h3>
Repeat the following tasks until you are satisified with the result:
<ol>
     <xsl:apply-templates/>
</ol>
</xsl:template>

<xsl:template match="branch">
<h3>
<li>
  <xsl:value-of select="translate(@name, '_', ' ')"/>
</li>
</h3>
Perform the following tasks in any order:
<ul>
     <xsl:apply-templates/>
</ul>
</xsl:template>

<xsl:template match="selection">
<h3>
<li>
  <xsl:value-of select="translate(@name, '_', ' ')"/>
</li>
</h3>
Perform exactly one of the following tasks:
<ul>
     <xsl:apply-templates/>
</ul>
</xsl:template>

<xsl:template match="sequence">
<h3>
<li>
  <xsl:value-of select="translate(@name, '_', ' ')"/>
</li>
</h3>
Peform the following tasks:
<ol>
     <xsl:apply-templates/>
</ol>
</xsl:template>


<xsl:template match="requires|provides">
 <xsl:value-of select="text()"/>
</xsl:template>

<xsl:template match="script">
 <xsl:apply-templates select="*|text()"/>
</xsl:template>

<xsl:template name="toc">
 <xsl:param name="title"/>
  <html>
   <head>
    <title><xsl:value-of select="$title"/></title>
    <xsl:call-template name="style"/>
   </head>
   <body>
    <xsl:call-template name="banner">
     <xsl:with-param name="title" select="$title"/>
    </xsl:call-template>

    <xsl:call-template name="nav-bar">
     <xsl:with-param name="next" select="child::action/@name"/>
    </xsl:call-template>

    <table style="width: 100%;" border="0" cellpadding="2" cellspacing="0">
     <tbody>
       <tr>
        <td style= "width: 25%; background-color: rgb(204, 204, 255);">
        </td>

	<td>
	
	 <hr/>

	 <h2>Table of Contents</h2>
	 <ol class="index">
	  <xsl:apply-templates/>
	 </ol>
	</td>
       </tr>
     </tbody>
    </table>

    <xsl:call-template name="nav-bar">
     <xsl:with-param name="next" select="child::action/@name"/>
    </xsl:call-template>

   </body>
  </html>
</xsl:template>

<xsl:template name="banner">
 <xsl:param name="title" select="'Your Process Name Here'"/>
 <xsl:param name="author" select="'Your Name Here'"/>
 <xsl:param name="institution" select="'Your Institution Name Here'"/>
<h1><xsl:value-of select="$title"/></h1>
<h2><xsl:value-of select="$author"/></h2>
<h3><i><xsl:value-of select="$institution"/></i></h3>
<hr/>
</xsl:template>

<xsl:template name="outline-pane">
 <xsl:param name="name" select="Process"/>
  <td style=
  "vertical-align: top; width: 25%; background-color: rgb(204, 204,
 255); overflow: auto; height: 10px;">
        <xsl:apply-templates mode="outline" select="/process"/>
  </td>
</xsl:template>

<xsl:template name="detail-pane">
 <td style="vertical-align: top; text-align: left;">

   <xsl:if test="boolean(requires)">
   <b>Requires: </b> <xsl:apply-templates select="requires"/><br/>
   </xsl:if>
   <xsl:if test="boolean(provides)">
   <b>Produces: </b> <xsl:apply-templates select="provides"/><br/>
   </xsl:if>
   <xsl:apply-templates select="script"/>
 </td>
</xsl:template>

<xsl:template name="nav-bar">
 <xsl:param name="next"/>
 <xsl:param name="prev"/>
 <xsl:param name="toc"/>

 <table style="text-align: left; background-color: rgb(255, 204, 51);
         width: 100%;"  cellpadding="1" cellspacing="1">
  <tbody>
   <tr>
    <td>
    <xsl:choose>
      <xsl:when test="not(boolean($prev))">
	&lt;&lt;Prev
      </xsl:when>
      <xsl:when test="count($prev) &gt; 0">
	<a href="{$prev}.html">	&lt;&lt;Prev </a>
      </xsl:when>
      <xsl:otherwise>
	&lt;&lt;Prev
      </xsl:otherwise>
    </xsl:choose>
    </td>

    <td>
    <xsl:choose>
      <xsl:when test="not(boolean($next))">
	Next&gt;&gt;
      </xsl:when>
      <xsl:when test="count($next) &gt; 0">
	<a href="{$next}.html">Next&gt;&gt;</a>
      </xsl:when>
      <xsl:otherwise>
	Next&gt;&gt;
      </xsl:otherwise>
    </xsl:choose>
    </td>	

    <xsl:if test="boolean($toc)">
     <td>
     <a href="{$toc}.html">TOC</a>
     </td>
    </xsl:if>
     <td>
     <a href="index.html">Home</a>
     </td>
    <td width="100%"></td>
   </tr>
  </tbody>
 </table>
</xsl:template>

<xsl:template name="footer">
  <table style="text-align: left; width: 100%;" 
  cellpadding="1" cellspacing="0">
    <tbody>
      <tr>
        <td style="background-color: rgb(255, 204, 51);">&amp;copy;2004
        Santa Clara University. Please direct your inquiries:
        <a href="mailto:jnoll@scu.edu">jnoll@scu.edu</a></td>
      </tr>
    </tbody>
  </table>
</xsl:template>



</xsl:stylesheet>

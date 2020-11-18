# Email Manager v 1.39

import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders


class EmailManager(object):
    """Email management class for formatting text, attachments, inline images, and sending messages."""

    def __init__(self):
        """EmailManager class initializer."""

        self.server_url = "mail.southernco.com"
        self.server_port = 25
        self.sender_address = "yourautomatedemail@southernco.com"
        self.primary_recipients = []
        self.cc_recipients = []
        self.body = ""
        self._inline_images = []
        self._attachments = []

    def add_text(self, text, bold = None, underline = None, italics = None, font_style = None, font_size = None, font_color = None, background_color = None, return_text = None):
        """Formats and adds the specified text to the email, or returns the formatted HTML text string.

        Args:
            text (string): Text to be added to the email.
            bold (bool): Optional flag to bold the text.
            underline (bool): Optional flag to underline the text.
            italics (bool): Optional flag to italicize the text.
            font_style (string): Optional name of the font style in which the text should be displayed.
            font_size (int): Optional size of the font in which the text should be displayed.
            font_color (string): Optional color name / hex code for the color of the text.
            background_color (string): Optional color name / hex code for the text background color.
            return_text (bool): Optional flag to return the formatted HTML text for further processing instead of appending it to the email text.

        Returns:
            string: Formatted HTML text string is returned if the return_text flag is set to true 
        """

        # Check for style options
        if font_style is not None or font_size is not None or font_color is not None or background_color is not None:
            style_string = ""
            
            if font_style is not None:
                style_string += "font-family: " + font_style + "; "

            if font_size is not None:
                style_string += "font-size: " + str(font_size) + "; "

            if font_color is not None:
                style_string += "color: " + font_color + "; "

            if background_color is not None:
                style_string += "background-color: " + background_color + "; "

            text = '<span style="' + style_string + '">' + text + "</span>"

        # Add bold, underline, and italics tags
        if bold:
            text = "<b>" + text + "</b>"

        if underline:
            text = "<u>" + text + "</u>"

        if italics:
            text = "<i>" + text + "</i>"

        # If the return_text flag is set to true, return the text, otherwise append to the email body
        if return_text:
            return text
        else:
            self.body += text

    def start_global_span(self, font_style = None, font_size = None, font_color = None, background_color = None, return_text = None):
        """Adds an unclosed span tag with the specified attributes, in order to encapsulate larger amounts of text that might be added in pieces.
        
        Args:
            font_style (string): Optional name of the font style in which the text should be displayed.
            font_size (int): Optional size of the font in which the text should be displayed.
            font_color (string): Optional color name / hex code for the color of the text.
            background_color (string): Optional color name / hex code to color the background of the text.
        """
        
        if font_style is not None or font_size is not None or font_color is not None or background_color is not None:
            global_style = '<span style="'

            if font_style is not None:
                global_style += "font-family: " + font_style + "; "

            if font_size is not None:
                global_style += "font-size: " + str(font_size) + "; "

            if font_color is not None:
                global_style += "color: " + font_color + "; "

            if background_color is not None:
                global_style += "background-color: " + background_color + "; "

            global_style = global_style + '">'
            self.body += global_style

    def close_global_span(self):
        """Writes a closing span tag to close off a global span."""

        self.body += "</span>"


    def add_break(self, num_breaks=None):
        """Adds a break tag at the current end of the email text.
        
        Args:
            num_breaks (int): Optional number of breaks to be added to the text. Defaults to 1.
        """

        if num_breaks is None:
            num_breaks = 1

        for i in range(0,num_breaks):
            self.body += "\n</br>\n"

    def add_table(self, headers, data, bold_headers = None, border = None, cell_padding = None, table_alignment = None, font_style = None, font_size = None, center_cells = None, cell_colors=None):
        """Creates an HTML table at the end of the current email text using a list of lists type data set.
        
        Args:
            headers (list): A list of row headers to use for the table.
            data (list of lists / list of dictionaries): The data set to be added to the table.
            bold_headers (bool): Optional flag to bold table headers.
            border (int): Optional specifier for the table border thickness.
            cell_padding (int): Optional specifier for the cell padding.
            table_alignment (string): Optional specifier for the alignment of the table within the email. Can be "left", "center", or "right".
            font_style (string): Optional name of the font style to use for the table.
            font_size (int): Optional specifier for the font size of the table.
            center_cells (bool): Optional flag to specify whether all text should be centered in their respective cells.
            cell_colors (bool): Optional flag to specify that the each cell of the input data is in a list format where the second element specifies individual cell color (i.e. [cell_data, color]).
        """

        table = "<table"

        # Check for style options
        if table_alignment is not None or font_style is not None or font_size is not None:
            style_string = ""

            if table_alignment == "left":
                style_string += "float: left; "
            elif table_alignment == "center":
                style_string += "margin-right: auto; margin-left: auto; "
            elif table_alignment == "right":
                style_string += "float: right; "

            if font_style is not None:
                style_string += "font-family: " + font_style + "; "

            if font_size is not None:
                style_string += "font-size: " + str(font_size) + "; "

            table += ' style="' + style_string + '"'

        # Check for table options
        if border is not None or cell_padding is not None:

            if border is not None:
                table += ' border="' + str(border) + '"'

            if cell_padding is not None:
                table += ' cellpadding="' + str(cell_padding) + '"'

        table += ">\n<tbody>\n<tr>\n"

        # Create table headers
        for header in headers:
            table += "<td"
            if center_cells:
                table += ' style="text-align: center;"'
            table += ">"
            if bold_headers:
                table += "<b>" + header + "</b>"
            else:
                table += header
            table += "</td>\n"
        table += "</tr>\n"

        # Check if data is of non zero length
        if len(data) > 0:
            # Data is in list of lists format, add each element to table
            if isinstance(data[0], list):
                for row in data:
                    table += "<tr>\n"
                    for cell in row:
                        table += "<td"
                        # Add style elements if either option is used
                        if center_cells is not None or cell_colors is not None:
                            table += ' style="'
                            if center_cells:
                                table += "text-align: center; "
                            if cell_colors:
                                # Add color name from the second element of the cell
                                table += "background-color: " + cell[1]
                            table += '"'
                        table += '>'
                        if cell_colors:
                            # Use the first cell element when a color is specified
                            table += str(cell[0]) + "</td>\n"
                        else:
                            # Colors not specified, so cell is one dimensional
                            table += str(cell) + "</td>\n"
                    table += "</tr>\n"
            # Data is in list of dicts format, loop through keys to add elements to table
            elif isinstance(data[0], dict):
                for row in data:
                    table += "<tr>\n"
                    for key in row.keys():
                        table += "<td"
                        # Add style elements if either option is used
                        if center_cells is not None or cell_colors is not None:
                            table += ' style="'
                            if center_cells:
                                table += "text-align: center; "
                            if cell_colors:
                                # Add color name from the second element of the cell
                                table += "background-color: " + row[key][1]
                            table += '"'
                        table += '>'
                        if cell_colors:
                            # Use the first cell element when a color is specified
                            table += str(row[key][0]) + "</td>\n"
                        else:
                            # Colors not specified, so cell is one dimensional
                            table += str(row[key]) + "</td>\n"
                    table += "</tr>\n"

        # Finish table and add
        table += "</tbody>\n</table>"
        self.body += table

    def add_bullet_list(self, data, seperator = None):
        """Adds an HTML bulleted list at the end of the current email text
        
        Args:
            data (list): List of data to be output to the bulleted list
            seperator (string): Optional seperator such as a dash (-) to seperate data items within a row. Defaults to a space.
        """

        if seperator is not None:
            _seperator = seperator
        else:
            _seperator = " "

        bullet_list = "<ul>\n"

        for row in data:
            bullet_list += "<li>" + _seperator.join(str(item) for item in row) + "</li>\n"

        bullet_list +=  "</ul>\n"
        self.body += bullet_list

    def add_inline_image(self, image_file_path):
        """Adds the specified inline image to the end of the current email text.
        
        Args:
            image_file_path (string): The file path of the inline image.
        """

        self._inline_images.append(image_file_path)
        self.body += '<img src="cid:%s">' % image_file_path

    def add_attachment(self, attachment_file_path):
        """Adds the specified file as an attachment to the current email.
        
        Args:
            attachment_file_path (string): The file path of the attachment.
        """

        self._attachments.append(attachment_file_path)

    def add_primary_recipient(self, email_address, is_string=None):
        """Adds an email address to the primary recipient list.
        
        Args:
            email_address (string): The email address to be added to the primary recipient list.
            is_string (bool): Optional flag to take input as a string of semicolon seperated email addresses (email1@domain.com; email2@domain.com...) rather than a single address. Set to false by default.
        """

        if is_string:
            email_address_list = email_address.replace(" ", "").split(";")
            for address in email_address_list:
                if address != "":
                    self.primary_recipients.append(address)
        else:
            self.primary_recipients.append(email_address)

    def clear_primary_recipients(self):
        """Deletes all primary recipients."""

        self.primary_recipients = []

    def add_cc_recipient(self, email_address, is_string=None):
        """Adds an email address to the CC recipient list.
        
        Args:
            email_address (string): The email address to be added to the CC recipient list. 
            is_string (bool): Optional flag to take input as a string of semicolon seperated email addresses ("email1@domain.com; email2@domain.com..."") rather than a single address. Set to false by default.
        """
        if is_string:
            email_address_list = email_address.replace(" ", "").split(";")
            for address in email_address_list:
                if address != "":
                    self.cc_recipients.append(address)
        else:
            self.cc_recipients.append(email_address)

    def clear_cc_recipients(self):
        """Deletes all CC recipients."""

        self.cc_recipients = []

    def send(self, subject):
        """Sends the current email along with all inline images and attachment files.
        
        Args:
            subject (string): The subject of the email to be sent.

        Raises
        """

        # Throw an exception if there are no primary recipients
        if len(self.primary_recipients) == 0:
            raise AttributeError("At least one primary recipient is required to send the email.")

        # Set up email
        server = smtplib.SMTP(self.server_url, self.server_port)
        email = MIMEMultipart()
        email["Subject"] = subject
        email["From"] = self.sender_address
        email.attach(MIMEText(self.body, "html"))

        # Build recipient strings
        primary_recipient_string = ""
        for address in self.primary_recipients:
            primary_recipient_string = primary_recipient_string + address + "; "

        cc_recipient_string = ""
        for address in self.cc_recipients:
            cc_recipient_string = cc_recipient_string + address + "; "

        email["To"] = primary_recipient_string
        email["Cc"] = cc_recipient_string

        # Add inline images
        for image in self._inline_images:
            image_file = open(image, "rb")
            mime_image = MIMEImage(image_file.read())
            image_file.close()
            mime_image.add_header("Content-ID", "<{}>".format(image))
            email.attach(mime_image)

        # Add attachments
        for attachment in self._attachments:
            mime_attachment = MIMEBase("application", "octet-stream")
            attachment_file = open(attachment, "rb")
            mime_attachment.set_payload(attachment_file.read())
            attachment_file.close()
            mime_attachment.add_header("Content-Disposition", 'attachment; filename ="' + attachment + '"')
            encoders.encode_base64(mime_attachment)
            email.attach(mime_attachment)

        server.sendmail(self.sender_address, self.primary_recipients + self.cc_recipients, email.as_string())
        server.close()

    def reset(self):
        """Completely resets the email so a new email can be created and sent."""
        
        self.primary_recipients = []
        self.cc_recipients = []
        self.body = ""
        self._inline_images = []
        self._attachments = []
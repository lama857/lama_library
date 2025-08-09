from datetime import datetime

class ReportMembership(models.AbstractModel):
    _name = 'report.lama_library.report_single_membership_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['library.membership'].browse(docids)
        return {
            'docs': docs,
            'report_date': datetime.today().strftime('%d/%m/%Y'),
        }
